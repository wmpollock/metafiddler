""" Verify pygame is happy """
import unittest
import pygame


class TestPygame(unittest.TestCase):
    """ Verify pygame components """

    def test_play(self):
        pygame.mixer.init()
        pygame.mixer.music.load("./tests/resources/spacemusic.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
