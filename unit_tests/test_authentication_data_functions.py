import pytest
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from unittest.mock import patch
from authentication_data_functions import *

passwords = [
    ("ArvrFEFEfer", False),
    ("aD!6", False),
    ("v00FG4cfC", False),
    ("5531@#", False),
    ("abcv&&@123B", True),
]

emails = [
    ("admin", False),
    ("admin@", False),
    ("admin.pl", False),
    ("admin@.pl", False),
    ("admin@o2.pl", True),
]

@pytest.mark.parametrize("input_, output_", passwords)
def test_is_valid_password(input_, output_):
    assert is_valid_password(input_) == output_


@pytest.mark.parametrize("input_, output_", emails)
def test_is_valid_email(input_, output_):
    assert is_valid_email(input_) == output_


@patch("authentication_data_functions.bcrypt.gensalt")
def test_hash_password(mock_salt):
    mock_salt.return_value = b'$2b$12$XK3FUEYcBzJ00ZoC8Q9rwe'

    hashed_password, salt = hash_password("password")

    assert salt == b'$2b$12$XK3FUEYcBzJ00ZoC8Q9rwe'
    assert hashed_password == bcrypt.hashpw(b"password", salt)






