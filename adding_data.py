from TestRail import APIClient
import configparser
import json
import re
import datetime


class TRInteract:

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")
        self.client = APIClient(self.config["TestRail"]["url"],
                                self.config["TestRail"]["username"],
                                self.config["TestRail"]["password"])
        self.info = ""
        self.status_code = int

    def get_cases(self, project_id: int) -> None:
        """
        The function receives data about all test cases in any project
        :param project_id: id of the chosen project
        """
        req_url = 'get_cases/' + str(project_id)
        self.info, self.status_code = self.client.send_get(req_url)

        if self.status_code == 200:
            print("Get info was successful")
        else:
            raise Exception("Error in getting info about cases:"
                            + str(self.status_code))

    @staticmethod
    def print_info(info: str) -> None:
        """
        Recording list of json in info.json for reading
        :param info: list of json data
        """
        with open("info.json", "a") as write_file:
            for i in info:
                json.dump(i, write_file, indent=4)

    def change_description(self) -> None:
        """
        Method changes or adds date in custom_preconds
        :param info: list of json with information about test cases
        """
        date = datetime.datetime.now().strftime("%d/%m/%Y")
        for test_case in self.info:
            preconds = test_case["custom_preconds"]
            match = re.search(r'\d{1,2}/\d{1,2}/\d{4}', preconds)
            if not match:
                test_case["custom_preconds"] += date
            else:
                test_case["custom_preconds"] = test_case["custom_preconds"].\
                    replace(match.group(), "")
                test_case["custom_preconds"] += date

    def post_description(self) -> int:
        """
        Sending modified data to the server
        :return: status_code
        """
        req_url = 'update_case/'
        status_code = list()

        for case in self.info:
            status_code.append(self.client.send_post
                               (uri=req_url + str(case["id"]), data=case))

        if not all(status_code):
            raise Exception("Warning, error updating descriptions")
        else:
            print("Post of descriptions was successful")

        return status_code

    def check_date(self) -> list:
        """
        The method checks for a date in description of test cases
        :return:
        If the data retrieval request was successful,
        it returns a list of items. In this case,
        True - if there is a date, False - if there is no date
        """
        date = list()
        if self.status_code == 200:
            for test_case in self.info:
                if not re.search(r'\d{1,2}/\d{1,2}/\d{4}',
                                 test_case["custom_preconds"]):
                    date.append(False)
                else:
                    date.append(True)
            return date
        return []


if __name__ == "__main__":
    attempt = TRInteract()
    attempt.get_cases(project_id=1)
    attempt.change_description()
    if attempt.check_date() is not []:
        attempt.post_description()
