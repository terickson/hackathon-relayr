Hackathon-Relayr
==================
This repo has examples of how to have a device deliver live relayr information and read that live data from relayr and broadcast it through socket-io to the web front-end
##Installation
* pip install -r requirements
* pip install git+https://github.com/relayr/python-sdk

##How To Use
* Open two terminal windows in the hackathon-relayr directory
* In the first run ./tempDevice.py to send (fake) temperature data to relayr
* In the second run ./broadDeviceInfo.py to get that data for relayr and then send it to the socket-io server for rebroadcast to all clients
* Then open the ui at: http://ciscohackathon2016.cloudapp.net and go to the Temperature page