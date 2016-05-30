from abstractRelayrDelegate import AbstractRelayrDelegate
import json
import time


class TempRelayrDelegate(AbstractRelayrDelegate):
    "A delegate class for temperature callbacks for an MQTT client."

    def __init__(self, credentials, publishing_period):
        super(TempRelayrDelegate, self).__init__(credentials, publishing_period)

    def create_message(self, temp):
        return self.base_message('temperature', temp)

    def send_data(self):
        while True:
            self.client.loop()
            message = self.create_message(40)
            self.client.publish(self.credentials['topic'] + 'data', json.dumps(message))
            time.sleep(self.publishing_period / 1000.)
