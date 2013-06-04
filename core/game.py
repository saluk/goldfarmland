import os,random,math

import pygame

from .world import World

from .agents import Text,Agent
from .ui import Button

import json

class ClickWorld(World):
    def input(self,controller):
        if controller.mbdown:
            x = controller.mpos[0]+self.offset[0]
            y = controller.mpos[1]+self.offset[1]
            for o in reversed(self.sprites):
                r = o.rect()
                if hasattr(o,"event_click") and x>=r.left and x<=r.right and y>=r.top and y<=r.bottom:
                    o.event_click()
                    return
        if controller.quit:
            self.engine.running = False

class LogoWorld(ClickWorld):
    def start(self):
        self.add(Button("art/icons/logo.png",self,"nextworld"))
    def nextworld(self):
        self.engine.world = GameWorld(self.engine)


class GameWorld(ClickWorld):
    pass

def make_world(engine):
    """This makes the starting world"""
    w1 = LogoWorld(engine)
    w = GameWorld(engine)
    return w1