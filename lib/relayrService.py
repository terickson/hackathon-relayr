from relayr import Client
from relayr.dataconnection import MqttStream


class RelayrService:
    def __init__(self, token, deviceId):
        # device 'fe4bb3e0-400f-48fa-aac0-0c2713a92827'
        #token 'FvhcUVcNkTsHqg4qI1w3wVs-Gadryj8O'
        self.client = Client(token=token)
        self.device = self.client.get_device(id=deviceId)

    def startStream(self, callback):
        self.stream = MqttStream(callback, [self.device])
        self.stream.start()

    def stopStream(self):
        self.stream.stop()
