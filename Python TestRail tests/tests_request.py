from request import Client
import configparser
from TestRail import APIClient
import time
import pytest

def config_data():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config


def find_by_key(data, key, value):
    for index, dict_ in enumerate(data):
        if key in dict_ and dict_[key] == value:
            return True
    return False


class TestRequest:
    config = config_data()
    main_url = config["TestRail"]["url_notAPI"]
    API_client = APIClient(config["TestRail"]["url"],
                           config["TestRail"]["username"],
                           config["TestRail"]["password"])
    req_url = 'get_users'
    add_data = {"name": config["TestRail"]["name"],
                "email": config["TestRail"]["email"],
                "notifications": config["TestRail"]["notifications"],
                "language": config["TestRail"]["language"],
                "theme": config["TestRail"]["theme"],
                "locale": config["TestRail"]["locale"],
                "timezone": config["TestRail"]["timezone"],
                "invite": config["TestRail"]["invite"],
                "password": config["TestRail"]["password"],
                "confirm": config["TestRail"]["password"],
                "role_id": config["TestRail"]["role_id"],
                "is_active": config["TestRail"]["is_active"],
                "js_test": config["TestRail"]["js_test"]}
    now = int(time.time())

    client = Client(main_url,
                    config["TestRail"]["username"],
                    config["TestRail"]["password"])

    def test_auth_with_correct_data(self):
        """
        Check the response of the Client class method
        when the auth data is entered correctly
        """
        client = Client(self.main_url,
                        self.config["TestRail"]["username"],
                        self.config["TestRail"]["password"])
        assert client.token is not None

    def test_auth_with_incorrect_data(self):
        """
        Check the response of the Client class method
        when the auth data is entered incorrectly
        """
        username = "Brad"
        with pytest.raises(Exception,
                           match="Failed to get token: "
                                 "'NoneType' object has no attribute 'get'"):
            Client(self.main_url, username,
                   self.config["TestRail"]["password"])

    def test_add_user_with_incorrect_data(self):
        """
        Check the add_user method for incorrectly entered data
        """
        buf_data = dict(self.add_data)
        buf_data["email"] = '1234'
        self.client.add_user(add_data=buf_data)
        info, status_code = self.API_client.send_get(self.req_url)
        assert find_by_key(info, "email", buf_data["email"]) is False

    def test_add_user_with_empty_data(self):
        """
        Check the add_user method
        with some empty element in data
        """
        buf_data = dict(self.add_data)
        del buf_data['email']
        buf_data['name'] = "Test" + str(self.now + 5)
        self.client.add_user(add_data=self.add_data)
        info, status_code = self.API_client.send_get(self.req_url)
        assert find_by_key(info, 'name', buf_data['name']) is False

    def test_added_user_in_test_rail(self):
        """
        Check
        if a new user appears after executing the add_user method
        """
        buf_data = dict(self.add_data)
        buf_data['name'] = "Test2" + str(self.now)
        buf_data['email'] = "Test2" + str(self.now) + "@gmail.com"
        res_status = self.client.add_user(add_data=buf_data)
        info, status_code = self.API_client.send_get(self.req_url)
        assert find_by_key(info, "email",
                           buf_data['email']) is True and res_status == 200
