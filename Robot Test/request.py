import requests
from bs4 import BeautifulSoup
import configparser
import time

config = configparser.ConfigParser()
config.read("config.ini")

main_url = config["TestRail"]["url_notAPI"]

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


class Client:
    """
    Class Client is used for authentication in TestRail and for adding and
    receiving information from this site
    """

    def __init__(self, base_url: str, user, password, rememberme=1):

        if not base_url.endswith('/'):
            base_url += '/'
        self.__url = base_url
        self.__auth_url = self.__url + "auth/login"
        self.__add_url = self.__url + "admin/users/add"
        self.sess = requests.Session()
        self.auth_data = {"name": user,
                          "password": password,
                          "rememberme": rememberme}
        self.token = None
        self.status_code = ""
        self.__auth()

    def __auth(self):
        """
        Authentication and token acquisition
        """
        self.status_code = self.sess.get(self.__auth_url).status_code
        if self.status_code == 200:
            self.status_code = self.sess.post(self.__auth_url,
                                              self.auth_data).status_code
            if self.status_code == 200:
                contents = self.sess.get(self.__url + "dashboard").content
                soup = BeautifulSoup(contents, 'lxml')
                try:
                    self.token = soup.find('input',
                                           {'name': '_token'}).get('value')
                except AttributeError as e:
                    raise Exception("Failed to get token: " + str(e))
                print("Auth was successful: " + str(self.status_code))
            else:
                raise Exception("Error in auth: " +
                                str(self.status_code))

        else:
            raise Exception("Access error: " +
                            str(self.status_code))

    def add_user(self, adding_data: dict) -> int:
        """
        Post request for adding the user
        :param adding_data: data for adding the user
        :return: status code
        """
        if self.token is not None:
            adding_data['_token'] = self.token
            response = self.sess.post(self.__add_url, adding_data)
            return response.status_code
        else:
            return 401


def make_client(url, username, password) -> Client:
    """
    Robot Framework keyword
    Instantiate Client class
    :param url: main url for connection
    :param username:
    :param password:
    :return: class
    """
    return Client(url, username,
                  password)


def time_create() -> int:
    """
    Robot Framework keyword
    Generate unix time
    :return: unix time
    """
    now = int(time.time())
    return now


def modify_return_data(unix: int) -> dict:
    """
    Robot Framework keyword
    Generate and return user information
    :param unix: unix time for user generation
    :return: dictionary with changed name and email
    """
    buf_data = dict(add_data)
    buf_data["name"] = "Test" + str(unix)
    print("Unix time: ", unix)
    buf_data["email"] = "Test" + str(unix) + "@gmail.com"
    return buf_data


if __name__ == "__main__":

    client = Client(main_url, config["TestRail"]["username"],
                    config["TestRail"]["password"])

    response_status = client.add_user(modify_return_data(time_create()))
    if response_status == 200:
        print("Adding user was successful")
    else:
        print("Authorization error")
