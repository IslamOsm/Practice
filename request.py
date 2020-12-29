import requests
from bs4 import BeautifulSoup
import configparser


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
        self.token = ""
        self.status_code = ""
        self.__auth()

    def __auth(self):
        """
        Authentication and token acquisition
        """
        if self.sess.get(self.__auth_url).status_code == 200:
            if self.sess.post(self.__auth_url,
                              self.auth_data).status_code == 200:

                contents = self.sess.get(self.__url + "dashboard").content
                soup = BeautifulSoup(contents, 'lxml')

                try:
                    self.token = soup.find('input',
                                           {'name': '_token'}).get('value')
                except AttributeError:
                    self.token = None
                    return

                self.status_code = 200
                print("Auth was successful: " + str(self.status_code))
            else:
                raise Exception("Error in auth: " +
                                str(self.sess.post(self.__auth_url,
                                                   self.auth_data)
                                    .status_code))

        else:
            raise Exception("Access error: " +
                            str(self.sess.get(self.__auth_url).status_code))

    def add_user(self, add_data: dict) -> int:
        """
        Post request for adding the user
        :param add_data: data for adding the user
        :return: status code
        """
        if self.token is not None:
            add_data['_token'] = self.token
            response = self.sess.post(self.__add_url, add_data)
            return response.status_code
        else:
            return 401


if __name__ == "__main__":
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

    client = Client(main_url, config["TestRail"]["username"],
                    config["TestRail"]["password"])
    response_status = client.add_user(add_data=add_data)
    if response_status == 200:
        print("Adding user was successful")
    else:
        print("Authorization error")
