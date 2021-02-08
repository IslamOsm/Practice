from mqtt_task import Client
import time
import configparser

config = configparser.ConfigParser()
config.read("mqtt_config.ini")
config = config["MQTT"]


class Publisher(Client):
    def __init__(self, username: str, password: str):
        super().__init__(username, password)
        self.client.on_publish = self.on_publish
        self.client.on_connect = self.on_connect_pub
        self.client.on_log = self.on_log
        self.client.on_disconnect = self.on_disconnect
        self.pub_QOS = int(config["pub_QOS"])
        self.client.connect(self.host, self.port, self.keepAlive)
        self.client.loop_start()

    def public_message(self, payload):
        """
        Call for sending info to the broker
        """
        time.sleep(2)
        print("Message: " + payload)
        self.client.publish(self.topic_name,
                            payload,
                            self.pub_QOS,
                            self.retain)

    def stop_publisher(self):
        """
        Stop publisher
        :return: None
        """
        self.client.loop_stop()
        self.client.disconnect()
