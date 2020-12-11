import requests
from bs4 import BeautifulSoup
import configparser


class Client:
    """
    CLient for TestRail interaction.
    """

    def __init__(self, base_url: str, email: str, password: str):
        """
        Initialize Client
        :param base_url: URL to TestRail
        :param email: TestRail user email for authentication
        :param password: TestRail user password for authentication
        :return: status code
        """  

        if not base_url.endswith('/'):
            base_url += '/'
        self.__url = base_url
        self.sess = requests.Session()
        self.auth_data = {"name": username,
                          "password": password, "rememberme": "1"}
        self.__auth()

    def __auth(self):
        """
        Authenticate user
        """
        auth_url = self.__url + "auth/login"
        ping_response = self.sess.get(auth_url)
        if ping_response.status_code == 200:
            auth_response = self.sess.post(auth_url, self.auth_data)
            if auth_response.status_code == 200:
                contents = self.sess.get(self.__url + "dashboard").content
                soup = BeautifulSoup(contents, 'lxml')
                self.token = soup.find(
                    'input', {'name': '_token'}).get('value')
                print("Succesfully authenticated to {}".format(self.__url))
            else:
                raise Exception(
                    "Error. Authentication Failed, response code: {}".format(
                        auth_response.status_code))
        else:
            raise Exception("Error. Unable to reach TestRail: {}".format(
                ping_response.status_code))

    def get_users(self) -> dict:
        """
        Get list of currently present users
        :return: dict with usernames and emails
        """
        get_users_url = self.__url + "admin/users/overview"
        contents = self.sess.get(get_users_url).content
        soup = BeautifulSoup(contents, 'lxml')
        res = soup.find("div", {"id": 'usersTable'})
        names = res.find_all("span", {"class": "name"})
        emails = res.find_all("span", {"class": "email"})
        users = dict()
        for name, email in zip(names, emails):
            users[name.get_text()] = email.get_text()
        return users

    def add_user(self, username: str, email: str) -> int:
        """
        Add user to TestRail with username and email
        :param username: username
        :param email: email
        :return: status code or None if failed to add user
        """
        current_users = self.get_users()
        if username in current_users.keys():
            print("User with name {} already exists".format(username))
            return None
        elif email in current_users.values():
            print("User with email {} already exists".format(email))
            return None
        
        add_url = self.__url + "admin/users/add"
        add_data = {"name": username, "email": email,
                    "confirm": self.auth_data["password"],
                    "password": self.auth_data["password"],
                    "_token": self.token,
                    "notifications": 1, "language": "en",
                    "theme": 0, "locale": "ru-ru", "timezone": "America/Godthab",
                    "invite": 1, "role_id": 1, "is_active": 1, "js_test": 1}

        response = self.sess.post(add_url, add_data)
        if response.status_code == 200:
            print("Succesfully added user: {}, {}".format(username, email))
        else:
            raise Exception(
                "Error adding user, response code {}".format(response.status_code))
        return response.content


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")
    tr_config = config["TestRail"]
    username = tr_config["username"]
    password = tr_config["password"]
    base_url = tr_config["url_notAPI"]

    client = Client(base_url, username, password)
    client.add_user("David Bowie", "db.official@nowhere.com")
