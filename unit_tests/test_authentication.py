import pytest
from unittest.mock import patch
import sys, os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from authentication import Authentication


@patch("database_connection.DatabaseConnection.execute_query")
def test_fetch_user_by_email(mock_database_execute__query):

    mock_database_execute__query.return_value = [True, (2, 'user@example.com', 'John Doe')]
    result = Authentication().fetch_user_by_email('user@example.com')

    assert result == [True, (2, 'user@example.com', 'John Doe')]


@patch("database_connection.DatabaseConnection.execute_query")
def test_create_new_user(mock_database_execute__query):

    mock_database_execute__query.return_value = True
    result = Authentication().create_new_user('user@example.com', 'hashed_password', b'salt')

    assert result is True

