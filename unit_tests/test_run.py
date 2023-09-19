import pytest
from unittest.mock import patch, Mock
import sys, os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from run import *


@pytest.mark.parametrize("cod", ["404", 200])
@patch("run.requests.get")
@patch.object(SelectQueryUtility, 'fetch_timer_by_user__email_and_hour')
@patch("run.get_credentials")
@patch("run.create_notification")
def test__get_request_called(_, mock_get_credentials, mock_select_query, mock_requests_get, cod):

    mocked_credentials = ["mocked_email", "mocked_password"]
    mock_get_credentials.return_value = mocked_credentials

    mock_select_query.return_value = (True, (["Warsaw", "Berlin"]))

    mock_response = Mock()
    mock_response.json.return_value = {"cod": cod}
    mock_requests_get.return_value = mock_response

    instance = HourlyScheduler()
    instance._get_request()

    mock_requests_get.assert_called()


@pytest.mark.parametrize("options", [
    (True, [[]]),
    (False, None)
])
@patch("run.requests.get")
@patch.object(SelectQueryUtility, 'fetch_timer_by_user__email_and_hour')
@patch("run.get_credentials")
def test__get_request_not_called(mock_get_credentials, mock_select_query, mock_requests_get, options):

    mocked_credentials = ["mocked_email", "mocked_password"]
    mock_get_credentials.return_value = mocked_credentials

    mock_select_query.return_value = options

    instance = HourlyScheduler()
    instance._get_request()

    mock_requests_get.assert_not_called()