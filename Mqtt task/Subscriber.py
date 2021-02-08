from mqtt_task import Client


class Subscriber(Client):
    def __init__(self, username: str, password: str):
        super().__init__(username, password)
        self.client.on_message = self.on_message
        self.client.on_log = self.on_log
        self.client.on_connect = self.on_connect_sub
        self.client.connect(self.host, self.port, self.keepAlive)

    def start_subscriber(self):
        self.client.loop_start()

    def return_messages(self):
        return self.messages

    def stop_subscriber(self):
        """
        Stop subscriber
        :return: None
        """
        self.client.loop_stop()
        self.client.disconnect()
