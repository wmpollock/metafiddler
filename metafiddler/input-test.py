import unittest
from metafiddler.input import Input
from metafiddler.events.input import Event


class TestConroller(unittest.TestCase):

    def test_controls(self):
        input = Input()
        e = input.poll()
        print("Gimme anyol input:")
        e = Event.NONE
        while e == Event.NONE:
            e = input.poll()

        print("Got event", Event.describe(e))
        return True
