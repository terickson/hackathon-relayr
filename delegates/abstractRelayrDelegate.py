from abc import ABCMeta, abstractmethod
import paho.mqtt.client as mqtt


class AbstractRelayrDelegate(object):
    "An abstract delegate class providing callbacks for an MQTT client."
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, credentials, publishing_period):
        self.credentials = credentials
        self.set_publishing_period(publishing_period)
        self.setup_client()

    def set_publishing_period(self, publishing_period):
        if publishing_period < 200:
            self.publishing_period = 200
        else:
            self.publishing_period = publishing_period

    def on_connect(self, client, userdata, flags, rc):
        print('Connected.')
        self.client.subscribe(self.credentials['topic'] + 'cmd')

    def on_message(self, client, userdata, msg):
        print('Command received: %s' % msg.payload)

    def on_publish(self, client, userdata, mid):
        print('Message published.')

    def base_message(self, meaning, value):
        return {
            'meaning': meaning,
            'value': value
        }

    def setup_client(self):
            self.client = mqtt.Client(self.credentials['clientId'])
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message
            self.client.on_publish = self.on_publish
            self.client.username_pw_set(self.credentials['user'], self.credentials['password'])
            self.client.connect(self.credentials['server'], port=self.credentials['port'], keepalive=60)

    @abstractmethod
    def send_data(self):
            pass
