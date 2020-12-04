import base64
import json
import requests
from bs4 import BeautifulSoup
from __init__ import testrail
import configparser


class Client:
    """
    Class Client is used for authentication in TestRail and for adding and receiving information from this site

    """
    def __init__(self, base_url):
        if not base_url.endswith('/'):
            base_url += '/'
        self.__url = base_url

    def create_session_add(self, auth_data: dict, auth_url: str, add_data: dict, add_url: str) -> int:
        """
        Creating session for adding the user
        :param auth_data: data for authentication
        :param auth_url: the link for authentication
        :param add_data: data for adding the user
        :param add_url: the link for adding the user
        """
        with requests.Session() as session:
            req = Client.__auth(sess=session, auth_data=auth_data, auth_url=auth_url, add_data=add_data,
                                base_url=self.__url)
            """
            req - variable that confirms receiving data from the request
            """


            if req is not None:
                adding = Client.__add_user(sess=session, add_data=req, add_url=add_url, m_url=self.__url)
                """
                adding - response from the server
                """
                if adding == 200:
                    return adding
            else:
                return -1

    @staticmethod
    def __auth(sess, auth_data: dict, auth_url: str, add_data: dict, base_url: str) -> dict:
        """
        The function to authenticate on the website
        :param sess: session for successful token receipt
        :param auth_data: data for authentication
        :param auth_url: the link for authentication
        :param add_data: data for adding the user
        :param base_url: the link for adding the user
        """
        req = sess.get(base_url + auth_url)
        if req.status_code == 200:
            if sess.post(base_url + auth_url, auth_data).status_code == 200:
                client = sess.get(base_url + "dashboard")
                contents = client.content
                soup = BeautifulSoup(contents, 'lxml')
                add_data['_token'] = soup.find('input', {'name': '_token'}).get('value')
                return add_data
            else:
                return None
        else:
            return None


    @staticmethod
    def __add_user(sess, add_data: dict, add_url: str, m_url: str) -> int:
        """
        Post request for adding the user
        :param sess: session for successful token receipt
        :param add_data: data for adding the user
        :param add_url: the link for authentication
        :param m_url: main url for adding the user
        :return:
        """
        print(m_url + add_url)
        req = sess.post(m_url + add_url, add_data)
        print(req.status_code)
        return req.status_code


class APIError(Exception):
    pass


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")

    client1 = testrail.APIClient(config["TestRail"]["url"])
    client1.user = config["TestRail"]["username"]
    client1.password = config["TestRail"]["password"]

# ---------------------------------------------------------
    main_url = config["TestRail"]["main_url"]

    add_data = {"name": "Islam Osmanov",
                "email": "osm152@gmail.ru",
                "notifications": "1",
                "language": "en", "theme": "0", "locale": "ru-ru", "timezone": "America/Godthab",
                "invite": "1", "role_id": "1", "is_active": "1", "js_test": "1"}

    auth_data = {"name": "ohjpnliamozfclsidc@wqcefp.online", "password": "dyFA5OwcSkUfmybCHZDx", "rememberme": "1"}

    client2 = Client(main_url)
    req = client2.create_session_add(auth_data=auth_data, auth_url="auth/login/", add_data=add_data,
                                     add_url="admin/users/add")

    if req == 200:
        print("Adding was successful")
    else:
        print("Mistake in adding")
