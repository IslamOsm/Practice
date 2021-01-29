from APIClient import APIClient
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
        Receive data about all test cases in any project
        :param project_id: id of the chosen project
        """
        req_url = 'get_cases/' + str(project_id)
        self.info, self.status_code = self.client.send_get(req_url)
        if self.status_code == 200:
            print("Get info was successful")
            return self.info
        else:
            raise Exception("Error in getting info about cases:"
                            + str(self.status_code))

    @staticmethod
    def print_info(info: str) -> None:
        """
        Record list of json in info.json for reading
        :param info: list of json data
        """
        with open("info.json", "a") as write_file:
            for i in info:
                json.dump(i, write_file, indent=4)

    def change_description(self, data) -> None:
        """
        Change or add date in custom_preconds
        :param data: some information for adding to the test case description
        """
        for case in self.info:
            description = case["custom_preconds"]
            match = re.search(r'\d{1,2}/\d{1,2}/\d{4}\s\d{2}:\d{2}:\d{2}',
                              description)
            if not match:
                case["custom_preconds"] += data
            else:
                case["custom_preconds"] = case["custom_preconds"].\
                    replace(match.group(), " ")
                case["custom_preconds"] += data

    def post_description(self) -> list:
        """
        Send modified data to the server
        :return: list of status_codes returned for cases descriptions update
        """
        req_url = 'update_case/'
        status_codes = list()

        for case in self.info:
            status_codes.append(self.client.send_post(uri=req_url +
                                                      str(case["id"]),
                                                      data=case))

        if not all(status_codes):
            raise Exception("Warning, error updating descriptions")
        else:
            print("Post of descriptions was successful")

        return status_codes

    def check_date(self, data: str) -> list:
        """
        Check for a date in description of test cases
        :param data: some information for checking
        :return:
        If the data retrieval request was successful,
        it returns a list of items. In this case,
        True - if there is a date, False - if there is no date
        """
        cur_date = list()
        if self.status_code == 200:
            for case in self.info:
                if not re.search(r'\d{1,2}/\d{1,2}/\d{4}\s\d{2}:\d{2}:\d{2}',
                                 case["custom_preconds"]):
                    cur_date.append(False)
                else:
                    if re.match(data, case["custom_preconds"]):
                        cur_date.append(True)
            return cur_date
        return []


def return_trinteract() -> TRInteract:
    """
    Robot Framework keyword
    Instantiate TRInteract class
    :return: class
    """
    return TRInteract()


def main_trinteract(current_date) -> int:
    """
    Robot Framework keyword
    Instantiate TRInteract class, get cases info, change description and
    post description
    :param current_date: current date
    :return: status code of post request
    """
    attempt = return_trinteract()
    attempt.get_cases(project_id=1)
    attempt.change_description(data=current_date)
    if attempt.check_date(data=current_date) is not []:
        attempt.post_description()
        return attempt.status_code


if __name__ == "__main__":
    date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(date)
    print(main_trinteract(date))
