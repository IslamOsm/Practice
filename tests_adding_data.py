import pytest
from adding_data import TRInteract
from TestRail import APIError


class TestTRInteract:
    tr_request = TRInteract()

    def test_get_cases_status_code(self):
        """
        Test cases checks correct request and server availability to get a list of test cases
        """
        self.tr_request.get_cases(project_id=1)
        assert self.tr_request.status_code == 200

    def test_wrong_get_cases_auth_status_code(self):
        """
        The test case checks the behavior of the get_cases function when data is entered incorrectly
        """
        with pytest.raises(APIError):
            self.tr_request.get_cases(project_id=2)

    def test_get_cases_data(self):
        """
        The test case checks for emptiness of the info variable to store data after the get request
        """
        self.tr_request.get_cases(project_id=1)
        assert len(self.tr_request.info) != 0

    def test_post_description(self):
        """
        Test case checks the success of the post request to change all test cases in the project to test rail
        """
        self.tr_request.get_cases(project_id=1)
        self.tr_request.change_description()
        assert all(self.tr_request.post_description()) is True

    def test_dates_in_cases(self):
        """
        The test case checks the date content in the test description
        """
        self.tr_request.get_cases(project_id=1)
        self.tr_request.change_description()
        dates = self.tr_request.check_date()
        assert False not in dates
