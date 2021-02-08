import paho.mqtt.client as mqtt
import time
import configparser

config = configparser.ConfigParser()
config.read("mqtt_config.ini")
config = config["MQTT"]


class Client:
    """
    Used for creating subscriber or publisher in process
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
        self.retain = False
        self.messages = list()
        self.client.username_pw_set(username=self.username,
                                    password=self.password)

    def on_connect_pub(self, pyClient, userdata, flags, rc) -> None:
        """
        Do connection to the broker for publisher
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

    def on_connect_sub(self, pvtClient, userdata, flags, rc) -> None:
        """
        Do connection to the broker for subscriber
        """
        if rc == 0:
            print("Connected to client! Return Code: " + str(rc))
            result = self.client.subscribe(self.topic_name, qos=2)
        elif rc == 5:
            print("Authentication Error! Return Code: " + str(rc))
            self.client.disconnect()

    def on_publish(self, client, userdata, mid) -> None:
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

    def on_disconnect(self, pvtClient, userdata, rc) -> None:
        """
        Called when the client disconnects from the broker
        """
        print("disconnecting reason  " + str(rc))
        self.client.disconnect()

    def on_message(self, pvtClient, userdata, msg) -> None:
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

        self.messages.append(str(msg.payload.decode()))
        print(self.messages)

        if msg.payload.decode() == "exit(0)":
            self.client.disconnect()

    def stop(self) -> None:
        """
        Stop client
        :return: None
        """
        self.client.loop_stop()
        self.client.disconnect()



