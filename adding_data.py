from TestRail import APIClient
import configparser
import json
import re
import datetime


class TRIntercat:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")
        self.client = APIClient(self.config["TestRail"]["url"], self.config["TestRail"]["username"],
                                self.config["TestRail"]["password"])

    @staticmethod
    def __update_and_post_descriptions(info, status_code):
        """

        :param info: data from get_cases
        :param status_code:
        :return: satus_code or None
        """
        info, size = TRIntercat.change_description(info)
        print(status_code)
        if status_code == 200:
            stat = TRIntercat().post_description(size, info)
            print(stat)
            return status_code
        else:
            return None

    def get_cases(self, id: int):
        """
        The function receives data about all test cases
        :param id: project id
        :return: info - list of json data, status_code
        """
        req_url = 'get_cases/' + str(id)
        print(req_url)
        info, status_code = self.client.send_get(req_url)
        TRIntercat.__update_and_post_descriptions(info, status_code)

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
    def change_description(info: list) -> str:
        """
        Function changes or adds date in custom_preconds
        :param info: list of json
        :return: info - modified data, len(info) - size of new data
        """
        now = datetime.datetime.now()
        date = " " + str(now.day) + "/" + str(now.month) + "/" + str(now.year)

        for i in info:
            preconds = i["custom_preconds"]
            match = re.search(r'\d{1,2}/\d{1,2}/\d{4}', preconds)
            if not match:
                i["custom_preconds"] += date
            else:
                i["custom_preconds"] = i["custom_preconds"].replace(match.group(), "")
                i["custom_preconds"] += date

        return info, len(info)

    def post_description(self, num_id: int, data: list) -> int:
        """
        Sending modified data to the server
        :param num_id: number of test cases' id
        :param data: modified data
        :return: status_code
        """
        req_url = 'update_case/'
        status_code = list()

        for id in range(0, num_id):
            req_url += str(id+1)
            status_code.append(self.client.send_post(uri=req_url, data=data[id]))
            req_url = req_url[0:-1]
        return status_code

    def check_date(self, url: str, num_id: int) -> dict:
        """

        :param url: link for GET request about every test cases
        :param num_id: number of id
        :return: list of bool
        """
        info, status_code = self.client.send_get(url + str(num_id))
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
    attempt = TRIntercat()
    attempt.get_cases(id=1)