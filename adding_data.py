from TestRail import APIClient
import configparser
import json
import re
import datetime

class ChangeInfo:

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")


    def get_cases(self, url: str, id: str):
        """
        The function receives data about all test cases

        :param url: link for getting data from server
        :param id: project id
        :return: info - list of json data, status_code
        """
        print(url + str(id))
        info, status_code = APIClient(self.config["TestRail"]["url"], self.config["TestRail"]["username"],
                                      self.config["TestRail"]["password"]).send_get(url + str(id))
        return info, status_code


    @staticmethod
    def print_info(info: str) -> None:
        """
        Recording list of json in info.json for reading
        :param info: list of json data
        :return:
        """
        with open("info.json", "a") as write_file:
            for i in info:
                json.dump(i, write_file, indent=4)

    @staticmethod
    def change_description(info: list) ->str:
        """
        Function changes or adds date in custom_preconds
        :param info: list of json
        :return: info - modified data, len(info) - size of new data
        """
        for i in info:
            preconds = i["custom_preconds"]
            if not re.search(r'\d{1,2}/\d{1,2}/\d{4}', preconds):
                print("check")
                now = datetime.datetime.now()
                date = " " + str(now.day) + "/" + str(now.month) + "/" + str(now.year)
                i["custom_preconds"] += date
            else:
                match = re.search(r'\d{1,2}/\d{1,2}/\d{4}', preconds)
                now = datetime.datetime.now()
                print(match.group())
                i["custom_preconds"] = i["custom_preconds"].replace(match.group(), "")
                date = " " + str(now.day) + "/" + str(now.month) + "/" + str(now.year)
                i["custom_preconds"] += date

        return info, len(info)


    def post_description(self, url:str, num_id: int, data:list) -> int:
        """
        Sending modified data to the server
        :param url: link for POST request
        :param num_id: number of test cases' id
        :param data: modified data
        :return: status_code
        """
        status_code = list()
        for i in range(num_id):
            url = url + str(i+1)
            status_code.append(APIClient(self.config["TestRail"]["url"], self.config["TestRail"]["username"],
                                         self.config["TestRail"]["password"]).send_post(uri=url, data=data[i]))
            url = url[0:-1]
        return status_code

    def check_date(self, url: str, num_id: int) -> dict:
        """

        :param url: link for GET request about every test cases
        :param num_id: number of id
        :return: list of bool
        """
        info, status_code = APIClient(self.config["TestRail"]["url"], self.config["TestRail"]["username"],
                                      self.config["TestRail"]["password"]).send_get(url + str(num_id))
        date = list()
        if status_code == 200:
            for i in info:
                if not re.search(r'\d{1,2}/\d{1,2}/\d{4}', i["custom_preconds"]):
                    date.append(False)
                else:
                    date.append(True)
            return date
        return []


if __name__ == "__main__":

    config = configparser.ConfigParser()
    config.read("config.ini")

    client = APIClient(base_url=config["TestRail"]["url"], user=config["TestRail"]["username"],
                       password=config["TestRail"]["password"])
    case, t = client.send_get('get_cases/1')

    attempt = ChangeInfo()
    info, status_code = attempt.get_cases(url='get_cases/', id=1)
    attempt.print_info(info)
    info, size = attempt.change_description(info)
    stat = attempt.post_description('update_case/', size, info)
    print(stat)



