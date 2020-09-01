import pygame
from pygame import joystick

from metafiddler.controller.interface import ControllerInterface

class Joystick(ControllerInterface):
    def __init__(self):
        joystick.init()
        self.count = joystick.get_count()
        print("Number of joysticks: {}".format(self.count))
        
        for index in range(self.count):
            stick = joystick.Joystick(index)
            stick.init()
            print("Setting up {}".format(stick.get_name()))
        
    def poll(self):
        """ Get a joystick event """
        event = pygame.event.get()

        if event.type == pygame.JOYBUTTONDOWN:
            print("BUTTON")
        elif event.type == pygame.JOYAXISMOTION:
            print("AXIS")    