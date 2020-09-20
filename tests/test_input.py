#!/bin/env python3

"""Providing for metafiddler.input"""

import unittest
from unittest.mock import Mock

import metafiddler.input
from metafiddler.input import Input
from metafiddler.input_events import InputEvent


class TestInput(unittest.TestCase):
    """Test controller functions"""

    def test_poll(self):
        """ Test the poll() event """
        metafiddler.input.controllers = [] 
        Input.poll(Mock(last_events=[InputEvent.NONE, InputEvent.NONE]))

if __name__ == "__main__":
    unittest.main()
