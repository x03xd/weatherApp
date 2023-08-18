import pytest
import sys, os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from setup import SetupHub

minutes = [
    ("g", False),
    ("3f", False),
    ("158", False),
    ("048", False),
    ("0068", False),
    ("001", False),
    ("03", True),
    ("3", True),
    ("23", True),
]


@pytest.mark.parametrize("input_, output", minutes)
def test__validate_minutes_method(input_, output):
    assert SetupHub._validate_minutes_method(input_) == output