#!/usr/bin/env python
import requests
from lib.relayrService import RelayrService
import json

baseUrl = 'http://ciscoHackathon2016.cloudapp.net:5000/event'
#baseUrl = 'http://localhost:5000/event'
token = 'pQHp-kTqHoT6jNGkrXJJspGRvF_ecBRs'
deviceIds = ['280dc96f-1e6b-49ad-b2ff-59897775f4cb']
#, 'f46dd0b3-2dc7-402c-a5bc-d56ae8e39977', '46a4fa64-ac35-4142-9b0a-e62ef4ca2c8f', 'c7db7583-e019-4194-98c2-51a57e7fd728']


class socketSetup:

    def __init__(self, event):
        self.event = event

    def socketIO_callback(self, topic, payload):
        payloadDict = json.loads(payload)
        for reading in payloadDict['readings']:
            data = {reading['meaning']: reading['value']}
            print(self.event)
            print(json.dumps(data))
            requests.post(baseUrl, {'event': self.event, 'data': data}, headers={'contentType': 'application/json'})

count = 1
for deviceId in deviceIds:
    tempRelayr = RelayrService(token, deviceId)
    socket = socketSetup('beeCountChange' + str(count))
    tempRelayr.startStream(socket.socketIO_callback)
    count += 1
while True:
    pass
