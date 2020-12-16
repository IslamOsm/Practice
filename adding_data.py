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
        self.info = ""
        self.status_code = int

    def get_cases(self, project_id: int):
        """
        The function receives data about all test cases in any project
        :param project_id: id os the choosen project
        """
        req_url = 'get_cases/' + str(project_id)
        self.info, self.status_code = self.client.send_get(req_url)

        if self.status_code == 200:
            print("Get info was successful")
        else:
            raise Exception("Error in getting info about cases:" + str(self.status_code))

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

    def change_description(self) -> str:
        """
        Function changes or adds date in custom_preconds
        :param info: list of json
        :return: info - modified data, len(info) - size of new data
        """
        now = datetime.datetime.now()
        date = " " + str(now.day) + "/" + str(now.month) + "/" + str(now.year)
        for test_case in self.info:
            preconds = test_case["custom_preconds"]
            match = re.search(r'\d{1,2}/\d{1,2}/\d{4}', preconds)
            if not match:
                test_case["custom_preconds"] += date
            else:
                test_case["custom_preconds"] = test_case["custom_preconds"].replace(match.group(), "")
                test_case["custom_preconds"] += date

    def post_description(self) -> int:
        """
        Sending modified data to the server
        :param num_id: number of test cases' id
        :param data: modified data
        :return: status_code
        """
        req_url = 'update_case/'
        status_code = list()

        for case in self.info:
            status_code.append(self.client.send_post(uri=req_url + str(case["id"]), data=case))

        if not all(status_code):
            raise Exception("Warning, error updating descriptions")
        else:
            print("Post was successful")

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
    attempt.get_cases(project_id=1)
    attempt.change_description()
    attempt.post_description()