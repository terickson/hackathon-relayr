#!/usr/bin/env python
from delegates.tempHackathonDelegate import TempHackathonDelegate

# mqtt credentials
creds = {
    'clientId': 'TeBwMy83xSDC4QhubXM89Pw',
    'user': '781c0ccb-cdf1-4830-b842-1b9b5ccf3d3f',
    'password': 'B_.gwp-_Gak0',
    'topic': '/v1/781c0ccb-cdf1-4830-b842-1b9b5ccf3d3f/',
    'server': 'mqtt.relayr.io',
    'port': 1883
}

publishing_period = 1000


if __name__ == '__main__':
    tempObj = TempHackathonDelegate(creds, publishing_period)
    tempObj.send_data()
