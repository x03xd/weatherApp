import pytest
from unittest.mock import patch
import sys, os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from common_query_utility import InsertQueryUtility, SelectQueryUtility, UpdateQueryUtility

@pytest.fixture
def mock_execute_query():
    with patch("database_connection.DatabaseConnection.execute_query") as mock:
        yield mock

def test_fetch_user_by_email(mock_execute_query):
    mock_result = [True, (2, "user@example.com", "hashed_password", "salt", "minutes_array")]
    mock_execute_query.return_value = mock_result

    instance = SelectQueryUtility("user@example.com")
    result = instance.fetch_user_by_email("*")

    mock_execute_query.assert_called_once()
    assert result == mock_result

def test_fetch_timer_by_user__email_and_hour(mock_execute_query):
    mock_result = [True, (["Warsaw", "Berlin"])]
    mock_execute_query.return_value = mock_result

    instance = SelectQueryUtility("user@example.com")
    result = instance.fetch_timer_by_user__email_and_hour("10")

    mock_execute_query.assert_called_once()
    assert result == mock_result


def test_is_user_logged_valid_credentials(mock_execute_query):
    mock_execute_query.return_value = [True, (2, "user@example.com", "hashed_password", "salt", "minutes_array")]
    result = SelectQueryUtility.is_user_logged(('test@example.com', 'hashed_password'))
    mock_execute_query.assert_called_once()

    assert result is True

def test_is_user_logged_invalid_credentials(mock_execute_query):
    mock_execute_query.return_value = (False, None)
    result = SelectQueryUtility.is_user_logged(('invalid@example.com', 'invalid_hashed_password'))
    mock_execute_query.assert_called_once()

    assert result is False



def test_restart_cities(mock_execute_query):
    instance = UpdateQueryUtility("user@example.com")
    instance.restart_cities()

    query = """UPDATE timers SET cities = '{}' WHERE user_email = %s;"""
    params = ("user@example.com",)
    mock_execute_query.assert_called_once_with(query, params, "UPDATE")


def test_restart_minutes_timers(mock_execute_query):
    instance = UpdateQueryUtility("user@example.com")
    instance.restart_minutes_timers()

    query = """UPDATE users SET minutes = '{}' WHERE email = %s;"""
    params = ("user@example.com",)
    mock_execute_query.assert_called_once_with(query, params, "UPDATE")


@pytest.mark.parametrize("operation", ["APPEND", "REMOVE"])
def test_update_user_minutes(mock_execute_query, operation):
    instance = UpdateQueryUtility("user@example.com")
    instance.update_user_minutes(operation, "12")

    query = f"""UPDATE users SET minutes = ARRAY_{operation}(minutes, %s) WHERE email = %s;"""
    params = ("12", "user@example.com")
    mock_execute_query.assert_called_once_with(query, params, "UPDATE")

@pytest.mark.parametrize("operation", ["APPEND", "REMOVE"])
def test_update_timer_city(mock_execute_query, operation):
    instance = UpdateQueryUtility("user@example.com")
    instance.update_timer_city("Warsaw", operation, "10")

    query = f"""UPDATE timers SET cities = ARRAY_{operation}(cities, %s) WHERE user_email = %s AND hour = %s;"""
    params = ("Warsaw", "user@example.com", "10")
    mock_execute_query.assert_called_once_with(query, params, "UPDATE")








def test_create_new_timer(mock_execute_query):
    mock_execute_query.return_value = True

    instance = InsertQueryUtility("user@example.com")
    result = instance.create_new_timer("10")

    mock_execute_query.assert_called_once()


'''def test_restart_cities(mock_execute_query):
    mock_execute_query

    expected_query = """UPDATE timers SET cities = '{}' WHERE user_email = %s;"""
    expected_params = ("test@example.com",)
    mock_execute_query.assert_called_once_with(expected_query, expected_params, "UPDATE")
'''