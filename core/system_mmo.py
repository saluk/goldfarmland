import random
import pygame

from . import systems
from .world import World,ClickWorld
from .ui import Button,TextButton
from .agents import Agent

class Char(Agent):
    def __init__(self):
        super().__init__("art/sprites/char.png")
    def load(self):
        super().load()
        self.subsurface([[0,0],[8,8]])
        self.surface = pygame.transform.scale(self.surface,[16,16])

class MMOWorld(ClickWorld):
    def __init__(self,manager,engine,game):
        super().__init__(engine)
        self.manager = manager
        self.game = game
        self.zone = systems.Zone("Test Zone",self.game,"grass")
        self.pc = Char()
        self.pc.pos = [5*32,5*32]
        self.add(self.pc)