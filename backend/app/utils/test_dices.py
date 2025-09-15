# tests/test_utils.py
import pytest
from dices import add_power

def test_add_same_dice():
    assert add_power("2d6", "3d6") == "5d6"

def test_add_different_dice():
    assert add_power("2d6", "1d8") == "2d6"  # different dice → return first

def test_invalid_input():
    assert add_power("", "3d6") == ""  # missing power1
    assert add_power("2d6", None) == "2d6"  # missing power2
    assert add_power("bad", "3d6") == "bad"  # invalid format
