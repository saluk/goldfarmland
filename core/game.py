import os,random,math

import pygame

from .world import World,ClickWorld,ManagerWorld

from .agents import Text,Agent
from .ui import Button
from . import systems
from .system_computer import ComputerWorld
from .system_apartment import ApartmentWorld

import json

class LogoWorld(ClickWorld):
    def start(self):
        self.add(Button("art/icons/logo.png",{"func":self.nextworld}))
    def nextworld(self):
        self.engine.world = GameWorld(self.engine)


class GameWorld(ManagerWorld):
    def __init__(self,engine):
        super().__init__(engine)
        self.computer = systems.Computer(speed=10,memory=10,harddrive=10)
        self.accounts = []
        self.visit_apartment()
    def accounts_for_game(self,game):
        return [x for x in self.accounts if x.game==game]
    def use_computer(self,computer):
        self.set_world(ComputerWorld(self,self.engine,computer))
    def visit_apartment(self):
        self.set_world(ApartmentWorld(self.computer,self,self.engine))

def make_world(engine):
    """This makes the starting world"""
    w = LogoWorld(engine)
    return w