# TMS_SIP_Email_Notification
Project to keep a check on SIP enpoints which gets unregistered and/or fails and to notify the same to the admin through an email to keep track of unregistered/failed endpoints and to find a resolution.

#### Author:

* Abhijith R (abhr@cisco.com)
*  June/July 2019
***

#### Prerequisites
* Python 3.X and its libraries
* PyCharm/Any text editor
* Flask
* Make sure you have a running TMS instance
* Make sure the endpoints are registered in the TMS instance

#### Steps to Reproduce
* Download/clone the repository
* Import the code into a text editor suck as pycharm
* Open controller.py file and make necessary changes as mentioned in the comments
* Import the virtual env(univ) into your development environment or you can setup your own with the necessary libraries
* After necessary changes are made to the code, execute/run controller.py file on the editor or on the terminal


#### API Reference/Documentation:
* [Cisco TelePresence Management Suite Extension Booking API](https://www.cisco.com/c/dam/en/us/td/docs/telepresence/infrastructure/tmsba/Cisco-TMSBA-API-guide-14-6.pdf)
* [Cisco Endpoint API Docs](https://www.cisco.com/c/dam/en/us/td/docs/telepresence/endpoint/api/collaboration-endpoint-software-api-transport.pdf)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.
