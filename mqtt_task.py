import paho.mqtt.client as mqtt
import time
import configparser

config = configparser.ConfigParser()
config.read("mqtt_config.ini")
config = config["MQTT"]


class Client:
    """
    Class Client is used for creating subscriber or publisher in process
    of communication with broker
    """
    def __init__(self, username: str, password: str):
        self.client = mqtt.Client()
        self.exitFlag = True
        self.host = config["host"]
        self.topic_name = config["topic_name"]
        self.port = int(config["port"])
        self.keepAlive = int(config["keepAlive"])
        self.username = username
        self.password = password
        self.retain = True
        self.client.username_pw_set(username=self.username,
                                    password=self.password)

    def on_connect_pub(self, pyClient, userdata, flags, rc):
        """
        The method does connection to the broker for publisher
        :param pyClient: the client instance for this callback
        :param userdata: the private user data as set in Client()
        :param flags: response flags sent by the broker
        :param rc: the connection result
        """
        if rc == 0:
            print("Client connected")
            self.exitFlag = False
        elif rc == 5:
            print("Authentication Error! Return Code: " + str(rc))
            self.client.disconnect()
            self.exitFlag = True

    def on_connect_sub(self, pvtClient, userdata, flags, rc):
        """
        The method does connection to the broker for subscriber
        """
        if rc == 0:
            print("Connected to client! Return Code: " + str(rc))
            result = self.client.subscribe(self.topic_name, qos=2)
        elif rc == 5:
            print("Authentication Error! Return Code: " + str(rc))
            self.client.disconnect()

    def on_publish(self, client, userdata, mid):
        """
        Called when a message that was to be sent using the publish()
        call has completed transmission to the broker.
        """
        print("Payload Published: " + str(mid))

    def on_log(self, client, userdata, level, buf):
        """
        Called when the client has log information
        """
        print("Logs: " + str(buf))

    def on_disconnect(self, pvtClient, userdata, rc):
        """
        Called when the client disconnects from the broker
        """
        print("disconnecting reason  " + str(rc))
        self.client.disconnect()

    def on_message(self, pvtClient, userdata, msg):
        """
        Called when a message has been received on a topic
        that the client subscribes to and the message does not match
        an existing topic filter callback
        """
        print("\n=========================")
        print("Payload: " + str(msg.payload.decode()))
        print("Qos of message: " + str(msg.qos))
        print("Message Topic : " + str(msg.topic))
        print("Message retain: " + str(msg.retain))
        print("============================\n")

        if msg.payload.decode() == "exit(0)":
            self.client.disconnect()


class Publisher(Client):
    def __init__(self, username: str, password: str):
        super().__init__(username, password)
        self.client.on_publish = self.on_publish
        self.client.on_connect = self.on_connect_pub
        self.client.on_log = self.on_log
        self.client.on_disconnect = self.on_disconnect
        self.pub_QOS = int(config["pub_QOS"])
        self.client.connect(self.host, self.port, self.keepAlive)

    def public_message(self):
        """
        Method is called for sending info to the broker
        """
        self.client.loop_start()
        time.sleep(2)
        while not self.exitFlag:
            time.sleep(.6)
            payload = input("\nMessage: ")
            self.client.publish(self.topic_name,
                                payload,
                                self.pub_QOS,
                                self.retain)
            if payload == "exit(0)":
                self.client.disconnect()
        self.client.loop_stop()


class Subscribe(Client):
    def __init__(self, username: str, password: str):
        super().__init__(username, password)
        self.client.on_message = self.on_message
        self.client.on_log = self.on_log
        self.client.on_connect = self.on_connect_sub

    def get_message(self):
        """
        Method is called for getting info from the broker
        """
        self.client.connect(self.host, self.port, self.keepAlive)
        time.sleep(2)
        self.client.loop_forever()


if __name__ == "__main__":
    choose = int(input("If you want to publish message enter the 0, "
                       "if you want to get message enter the 1: "))
    if choose == 0:
        publ_username = config["publ_username"]
        publ_password = config["publ_password"]
        publ = Publisher(publ_username, publ_password)
        publ.public_message()
    elif choose == 1:
        sub_username = config["sub_username"]
        sub_password = config["sub_password"]
        sub = Subscribe(sub_username, sub_password)
        sub.get_message()

