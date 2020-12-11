import requests
from bs4 import BeautifulSoup
import configparser


class Client:
    """
    Class Client is used for authentication in TestRail and for adding and receiving information from this site
    """


    def __init__(self, base_url: str, username: str, password: str):
        
        self.sess = requests.Session()
        if not base_url.endswith('/'):
            base_url += '/'
        self.__url = base_url
        self.auth_data = {"name": username, "password": password, "rememberme": "1"}
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
                self.token = soup.find('input', {'name': '_token'}).get('value')
                print("Succesfully authenticated to {}".format(self.__url))
            else:
                raise Exception("Error. Authentication Failed, response code: " + str(auth_response.status_code))
        else:
            raise Exception("Error. Unable to reach TestRail: " + str(ping_response.status_code))


    def add_user(self, username: str, email: str) -> int:
        """
        Add user to TestRail with username and email
        :param username: username
        :param email: email
        :return: status code
        """
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
            raise Exception("Error adding user, response code {}".format(response.status_code))
        return response.content

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")
    tr_config = config["TestRail"]
    main_url = tr_config["url_notAPI"]

    # add_data = {"name": tr_config["TestRail"]["name"],
    #             "email": tr_config["TestRail"]["email"],
    #             "notifications": tr_config["TestRail"]["notifications"],
    #             "language": tr_config["TestRail"]["language"],
    #             "theme": config["TestRail"]["theme"],
    #             "locale": config["TestRail"]["locale"],
    #             "timezone": config["TestRail"]["timezone"],
    #             "invite": config["TestRail"]["theme"], "password": config["TestRail"]["password"],
    #             "confirm": config["TestRail"]["password"],
    #             "role_id": config["TestRail"]["role_id"],
    #             "is_active": config["TestRail"]["is_active"],
    #             "js_test": config["TestRail"]["js_test"]}
    
    username = tr_config["username"]
    password = tr_config["password"]

    client = Client(main_url, username, password)
    client.add_user("David Bowie","DB.official@nowhere.com")
