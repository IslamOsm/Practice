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
        self.retain = True
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

        if msg.payload.decode() == "exit(0)":
            self.client.disconnect()

    def stop(self) -> None:
        """
        Stop client
        :return: None
        """
        self.client.loop_stop()
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


class Subscribe(Client):
    def __init__(self, username: str, password: str):
        super().__init__(username, password)
        self.client.on_message = self.on_message
        self.client.on_log = self.on_log
        self.client.on_connect = self.on_connect_sub
        self.client.connect(self.host, self.port, self.keepAlive)

    def get_message(self):
        """
        Call for getting info from the broker
        """
        time.sleep(1)
        self.client.loop_start()
        time.sleep(1)


def generate_publisher() -> Publisher:
    """
    Robot Framework keyword
    Instantiate Publisher class
    :return: class
    """
    publ_username = config["publ_username"]
    publ_password = config["publ_password"]
    publish = Publisher(publ_username, publ_password)
    return publish


def generate_subscriber() -> Subscribe:
    """
    Robot Framework keyword
    Instantiate Subscribe class
    :return: class
    """
    sub_username = config["sub_username"]
    sub_password = config["sub_password"]
    subscribe = Subscribe(sub_username, sub_password)
    return subscribe


def get_message(subscribe) -> None:
    """
    Get message from the topic
    :param subscribe: class of Subscribe
    :return: None
    """
    subscribe.get_message()


def return_list_messages(subscribe) -> None:
    """
    Robot Framework keyword
    :param subscribe: class of Subscribe
    :return: None
    """
    return subscribe.messages


def send_message(message: str, publish) -> None:
    """
    Robot Framework keyword
    :param message: sending message
    :param publish: class Publisher
    :return: None
    """
    publish.public_message(message)


def stop(client) -> None:
    """
    Robot Framework keyword
    Stop client action
    :param client: class Subscribe or Publisher
    :return: None
    """
    client.stop()


if __name__ == "__main__":

    subscriber = generate_subscriber()
    publisher = generate_publisher()

    send_message("Hi", publisher)
    time.sleep(3)
    get_message(subscriber)
    send_message("Ho", publisher)
    time.sleep(3)
    get_message(subscriber)

    print(return_list_messages(subscriber))

    stop(publisher)
    stop(subscriber)
