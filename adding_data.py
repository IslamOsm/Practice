from TestRail import APIClient
import configparser
import json
import re
import datetime


class TRInteract:
    def __init__(self, config_file: str):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.config = self.config["TestRail"]
        self.client = APIClient(self.config["url"], self.config["username"],
                                self.config["password"])

    def update_descriptions(self, project_id: int,
                            modify_cases_data: dict):
        """
        :param info: data from get_cases
        :param status_code:
        :return: satus_code or None
        """
        cases = self.get_cases(project_id)
        mod_case_ids = [int(c_id) for c_id in modify_cases_data.keys()]
        updated_cases = list()
        for case in cases:
            if case["id"] in mod_case_ids:
                add_data = modify_cases_data[str(case["id"])]
                case = self.modify_descriptions(case, add_data)
                updated_cases.append(case)
        self.post_descriptions(updated_cases)
        return updated_cases

    def modify_description(self, case: dict, data: str,
                            selector: str = "custom_comments") -> dict:
        section = case[selector]
        add_string = "Additional info: {}".format(data)
        if section is None:
            section = add_string
        else:
            match = re.search(r"Additional info:.*", section)
            if match:
                section = section.replace(match.group(), add_string)
            else:
                section += "\n" + add_string
        case[selector] = section
        return case

    def get_cases(self, project_id: int) -> list:
        """
        Get test cases for project
        :param project_id: project id
        :return: list of json data
        """
        req_url = 'get_cases/{}'.format(project_id)
        cases = self.client.send_get(req_url)[0]
        # print(cases)
        return cases

    def post_descriptions(self, modified_cases: list) -> list:
        """
        Sending modified data to the server
        :param num_id: number of test cases' id
        :param data: modified data
        :return: status_codes
        """
        req_url = 'update_case/'
        status_codes = list()

        for case in modified_cases:
            case_id = str(case["id"])
            status_codes.append(self.client.send_post(
                req_url + case_id, data=case))

        if not all(status_codes):
            print("Warning, error updating descriptions")

        return status_codes

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


if __name__ == "__main__":
    testrail_client = TRInteract("config.ini")
    cases = testrail_client.get_cases(1)
    # print("Test Cases:", cases)
    date = datetime.datetime.now()
    testrail_client.update_descriptions(1, {"1": date})
