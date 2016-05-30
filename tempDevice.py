#!/usr/bin/env python
from delegates.tempRelayrDelegate import TempRelayrDelegate

# mqtt credentials
creds = {
    'clientId': 'To6Du7G0lRtSm+0dERmVLsQ',
    'user': 'a3a0eeec-6d25-46d4-a6fb-474446654bb1',
    'password': 's9tWXtYFdDHx',
    'topic': '/v1/a3a0eeec-6d25-46d4-a6fb-474446654bb1/',
    'server': 'mqtt.relayr.io',
    'port': 1883
}

publishing_period = 1000


if __name__ == '__main__':
    tempObj = TempRelayrDelegate(creds, publishing_period)
    tempObj.send_data()
