import unittest
from adding_data import ChangeInfo
import configparser
import re

class TestRequests(unittest.TestCase):

    def config_data(self):
        """
        Function for connecting to the config.ini
        :return: config - configuration
        """
        config = configparser.ConfigParser()
        config.read("config.ini")
        return config

    def test_get_request(self):
        """
        1-st test checks correct request and server availability to get a list of test cases
        2-nd test checks data retrieval
        """
        config = TestRequests().config_data()
        self.assertEqual(int(ChangeInfo().get_cases(config["TestRail"]["get_cases"], 1)[1]), 200)
        self.assertEqual(bool(ChangeInfo().get_cases(config["TestRail"]["get_cases"], 1)[0]), True)

    def test_change_description(self):
        """
        1)Testing the correctness of the function for finding a date in a string
        2)Testing of returning the required amount of changed data
        """
        config = TestRequests().config_data()
        self.assertEqual(re.search(r'\d{1,2}/\d{1,2}/\d{4}', "Hello, world!! 14/12/2020").group(), '14/12/2020')
        self.assertEqual(ChangeInfo().change_description(ChangeInfo().get_cases(config["TestRail"]["get_cases"], 1)
                         [0])[1], 2)

    def test_check_date(self):
        config = TestRequests().config_data()
        """
        1)Testing presence of dates in the description of test cases
        """
        self.assertEqual(ChangeInfo().check_date(config["TestRail"]["get_cases"], 1), [True, True])
