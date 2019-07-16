#!/usr/bin/env python3

"""
Copyright (c) 2019 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.0 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

"""

import requests
import smtplib
import xml.etree.ElementTree as ET
import atexit
import urllib3
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


app = Flask(__name__)

# Change the credentials below as per requiremen
tms_ip = "Your TMS IP"
tms_username = "TMS Username"
tms_password = "TMS Password"


def get_device_ip_from_tms():
    # Function to fetch IP from TMS
    url = "https://"+tms_ip+"/tms/external/booking/remotesetup/remotesetupservice.asmx?wsdl"
    # headers = {'content-type': 'application/soap+xml'}
    headers = {'content-type': 'text/xml'}
    body = """<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
      <soap:Header>
        <ExternalAPIVersionSoapHeader xmlns="http://tandberg.net/2004/02/tms/external/booking/remotesetup/">
          <ClientVersionIn>22</ClientVersionIn>
          <ClientIdentifierIn>test</ClientIdentifierIn>
          <ClientLatestNamespaceIn>test2</ClientLatestNamespaceIn>
          <NewServiceURL>string</NewServiceURL>
          <ClientSession>s2</ClientSession>
        </ExternalAPIVersionSoapHeader>
      </soap:Header>
      <soap:Body>
        <GetSystems xmlns="http://tandberg.net/2004/02/tms/external/booking/remotesetup/" />
      </soap:Body>
    </soap:Envelope>"""
    try:
        response = requests.post(url, data=body,headers=headers, auth=requests.auth.HTTPBasicAuth(tms_username, tms_password), verify = False)
        ip = {}
        if response.status_code == 200:
            tree = ET.ElementTree(ET.fromstring(response.text))
            root = tree.getroot()
            for elem in root.iter("{http://tandberg.net/2004/02/tms/external/booking/remotesetup/}WebInterfaceURL"):
                ip[elem.text] = "0"
            return ip
        else:
            print("Unexpected error in fetching the IPs from TMS with status code " +str(response.status_code))
            exit()
    except Exception as e:
        print("Unexpected error "+str(e))


endpoint_ip = get_device_ip_from_tms()  # Store the IP and the notification status flag



def set_flag(ip):
    # Set flag to 1 if a unregistered device is already notified
    for k in endpoint_ip.__iter__():
        endpoint_ip[ip] = "1"


def unset_flag(ip):
    # Unset flag if device is registered
    for k in endpoint_ip.__iter__():
        if(endpoint_ip[ip] == "1"):
            endpoint_ip[ip] = "0"
            send_email_notification(ip.rstrip('/'), "back online")


def get_sip_status(ip):
    # Function to fetch SIP registration status from the endpoint

    endpoint_username = "Endpoint Username" # change username of the endpoint
    endpoint_password = "Endpoint password" # change password of the endpoint
    url = "https://"+ip+"/status.xml"
    headers = {'content-type': 'text/xml'}
    device_details = {}
    response = requests.get(url, headers=headers,
                             auth=requests.auth.HTTPBasicAuth(endpoint_username, endpoint_password), verify=False)
    if response.status_code == 200:
        tree = ET.ElementTree(ET.fromstring(response.text))
        root = tree.getroot()
        for name in root.iter('UserInterface'):
            dev_name = name.find("ContactInfo").find("Name")
        for status in root.iter('SIP'):
            stat = status.find("Registration").find("Status")
        device_details[dev_name.text] = stat.text
        return device_details
    else:
        print("Unexpected error getting the SIP status with error code "+str(response.status_code))
        exit()


def send_email_notification(devname, sipstatus):
    # Function to send email notification if a SIP device is unregistered
    # Change the below details as needed
    fromaddr = "from@example.com"
    toaddrs = "to@example.com"
    mailserver_username = "test@example.com"
    mailserver_password = "password"
    mailserver = smtplib.SMTP('smtp.office365.com', 587) # mail server as required
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.login(mailserver_username, mailserver_password)
    header = 'To:' + toaddrs + '\n' + 'From: ' + fromaddr + '\n' + 'Subject:Alert: SIP Notification \n'
    print(header)
    msgbody = header + "\n Kindly note "+devname+" device is "+sipstatus+"\n"
    mailserver.sendmail(fromaddr, toaddrs, msgbody)
    mailserver.quit()

def main():
    for ip,flag in endpoint_ip.items():
        sipdetails = get_sip_status(ip)
        for key in sipdetails.__iter__():
            if sipdetails.get(key) == "Registered":
                print("Registered")
                unset_flag(ip)
            else:
                if flag == "1":
                    print("Already notified")
                else:
                    set_flag(ip)
                    print("Send email notification")
                    send_email_notification(key, sipdetails.get(key))
    print(endpoint_ip)



scheduler = BackgroundScheduler()
scheduler.add_job(func=main, trigger="interval", seconds=60)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
    app.run()