#!/usr/bin/env python
from socketIO_client import SocketIO
from lib.relayrService import RelayrService
import json

socketIO = SocketIO('ciscoHackathon2016.cloudapp.net', 5000)
token = 'FvhcUVcNkTsHqg4qI1w3wVs-Gadryj8O'
deviceId = 'a3a0eeec-6d25-46d4-a6fb-474446654bb1'


def resp_callback(*args):
    print('my event response', args)


def socketIO_callback(topic, payload):
    payloadDict = json.loads(payload)
    for reading in payloadDict['readings']:
        data = {reading['meaning']: reading['value']}
        print(json.dumps(data))
        socketIO.emit('broadcast', {'event': 'tempData', 'data': data})


tempRelayr = RelayrService(token, deviceId)
socketIO.on('my response', resp_callback)
tempRelayr.startStream(socketIO_callback)
while True:
    pass
