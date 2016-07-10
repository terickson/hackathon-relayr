from abstractRelayrDelegate import AbstractRelayrDelegate
import json
import time
import requests
from pprint import pprint


class TempHackathonDelegate(AbstractRelayrDelegate):
    "A delegate class for temperature callbacks for an MQTT client."

    def __init__(self, credentials, publishing_period):
        super(TempHackathonDelegate, self).__init__(credentials, publishing_period)
        self.alertStatus = False
        self.alertThreshold = 60.0
        self.phoneNumbers = ['13145291038']
        self.alertMessage = 'Hello, Your Beehive seems to be in a bad state.  Please check it immediately.'

    def create_message(self):
        request_data = requests.get('http://guidoslabs.com/sensorFiles/temperature.txt')
        #return self.base_message('temperature', float(99.9))
        return self.base_message('temperature', float(request_data.text))

    def socketIO_callback(self, data):
        print 'calling1'
        url = 'http://prod--hackathon2016--hackathon-api--bc5588.gce.shipped-cisco.com/sensors/hiveTemp'
        #url = 'http://localhost:5000/sensors/hiveTemp'
        print 'temperature: ' + str(data['temperature'])
        mappedData = {'name': 'hiveTemp', 'value': data['temperature']}
        requestResp = requests.put(url, mappedData, headers={'Content-Type': 'application/json'})
        print 'requestResponse: ' + str(requestResp)
        print 'calling2'

    def check_alert_status(self, data):
        print 'temperature: ' + str(data['temperature'])
        if data['temperature'] <= self.alertThreshold and not self.alertStatus:
            alertAction = {'type': 'tropo', 'phoneNumbers': self.phoneNumbers, 'message': self.alertMessage}
            url = 'http://prod--hackathon2016--hackathon-api--bc5588.gce.shipped-cisco.com/actions'
            headers = {'content-type': 'application/json'}
            alertResp = requests.post(url, data=json.dumps(alertAction), headers=headers)
            pprint(alertResp)
            pprint(json.dumps(alertAction))
        if data['temperature'] <= self.alertThreshold:
            self.alertStatus = True
        else:
            self.alertStatus = False

    def send_data(self):
        while True:
            self.client.loop()
            message = self.create_message()
            mapData = {message['meaning']: message['value']}
            self.socketIO_callback(mapData)
            self.check_alert_status(mapData)
            self.client.publish(self.credentials['topic'] + 'data', json.dumps(message))
            time.sleep(self.publishing_period / 1000.)
