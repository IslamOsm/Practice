import base64
import json
import requests
from bs4 import BeautifulSoup


class APIClient:
    def __init__(self, base_url):
        self.user = ''
        self.password = ''
        if not base_url.endswith('/'):
            base_url += '/'
        self.__url = base_url + 'index.php?/'

    def send_get(self, uri, filepath=None):
        return self.__send_request('GET', uri, filepath)

    def send_post(self, uri, data):
        return self.__send_request('POST', uri, data)

    def __send_request(self, method, uri, data):
        url = self.__url + uri
        print(url)
        auth = str(
            base64.b64encode(
                bytes('%s:%s' % (self.user, self.password), 'utf-8')
            ),
            'ascii'
        ).strip()
        headers = {"Authorization" : "Basic " + auth}

        if method == 'POST':
            if uri[:14] == 'add_attachment':    # add_attachment API method
                files = {'attachment': (open(data, 'rb'))}
                response = requests.post(url, headers=headers, files=files)
                files['attachment'].close()
            else:
                print("qwe")
                headers['Content-Type'] = 'application/json'
                payload = bytes(json.dumps(data), 'utf-8')
                print(payload)
                print(headers)

                response = requests.post(url, headers=headers, data=payload)
                print(response)
        else:
            headers['Content-Type'] = 'application/json'
            response = requests.get(url, headers=headers)
            print(response.content)

        if response.status_code > 201:
            try:
                error = response.json()
            except:     # response.content not formatted as JSON
                error = str(response.content)
            raise APIError('TestRail API returned HTTP %s (%s)' % (response.status_code, error))
        else:
            if uri[:15] == 'get_attachment/':   # Expecting file, not JSON
                try:
                    open(data, 'wb').write(response.content)
                    return (data)
                except:
                    return ("Error saving attachment.")
            else:
                print("Hello")
                try:
                    return response.json()
                except:# Nothing to return
                    return {}


class Client:
    def __init__(self, base_url):
        if not base_url.endswith('/'):
            base_url += '/'
        self.__url = base_url

    def creating_session_adding(self, auth_data: dict, auth_url: str, add_data: dict, add_url: str) -> int:
        with requests.Session() as session:
            req = Client.__auth(sess=session, auth_data=auth_data, auth_url=auth_url, add_data=add_data,
                                base_url=self.__url)
            print(req)
            if req is not None:
                adding = Client.__adding_user(sess=session, add_data=req, add_url=add_url, m_url=self.__url)
                if adding == 200:
                    return adding
            else:
                return -1

    @staticmethod
    def __auth(sess, auth_data: dict, auth_url: str, add_data: dict, base_url: str) -> dict:
        req = sess.get(base_url + auth_url)
        if req.status_code == 200:
            if sess.post(base_url + auth_url, auth_data).status_code == 200:
                client = sess.get(base_url + "dashboard")
                open("client.html", "wb").write(client.content)
                with open("client.html", "r") as f:
                    contents = f.read()
                    soup = BeautifulSoup(contents, 'lxml')
                    add_data['_token'] = soup.find('input', {'name': '_token'}).get('value')
                return add_data
            else:
                return None
        else:
            return None


    @staticmethod
    def __adding_user(sess, add_data: dict, add_url: str, m_url: str) -> int:
        print(m_url + add_url)
        req = sess.post(m_url + add_url, add_data)
        print(req.status_code)
        return req.status_code


class APIError(Exception):
    pass


if __name__ == "__main__":
    url = "https://ohjpnliamozfclsidc.testrail.io/"
    Cl = APIClient(url)
    Cl.user = "ohjpnliamozfclsidc@wqcefp.online"
    Cl.password = "dyFA5OwcSkUfmybCHZDx"
# ---------------------------------------------------------
    main_url = "https://ohjpnliamozfclsidc.testrail.io/index.php?/"

    add_data = {"name": "Islam Osmanov",
                "email": "osm152@gmail.ru",
                "notifications": "1",
                "language": "en", "theme": "0", "locale": "ru-ru", "timezone": "America/Godthab",
                "invite": "1", "role_id": "1", "is_active": "1", "js_test": "1"}

    auth_data = {"name": "ohjpnliamozfclsidc@wqcefp.online", "password": "dyFA5OwcSkUfmybCHZDx", "rememberme": "1"}

    client1 = Client(main_url)
    req = client1.creating_session_adding(auth_data=auth_data, auth_url="auth/login/", add_data=add_data,
                                          add_url="admin/users/add")

    if req == 200:
        print("Adding was successful")
    else:
        print("Mistake in adding")
