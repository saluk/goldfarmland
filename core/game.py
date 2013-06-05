import os,random,math

import pygame

from .world import World,ClickWorld,ManagerWorld

from .agents import Text,Agent
from .ui import Button
from . import systems
from .system_computer import ComputerWorld

import json

class LogoWorld(ClickWorld):
    def start(self):
        self.add(Button("art/icons/logo.png",self,"nextworld"))
    def nextworld(self):
        self.engine.world = GameWorld(self.engine)


class GameWorld(ManagerWorld):
    def __init__(self,engine):
        super().__init__(engine)
        self.computer = systems.Computer(speed=10,memory=10,harddrive=10)
        self.use_computer(self.computer)
    def use_computer(self,computer):
        self.set_world(ComputerWorld(self.engine,computer))

def make_world(engine):
    """This makes the starting world"""
    w = LogoWorld(engine)
    return w