import random
import pygame

from . import systems
from .world import World,ClickWorld
from .ui import Button,TextButton
from .agents import Agent

class Char(Agent):
    def __init__(self,index=[[0,0],[8,8]]):
        super().__init__("art/sprites/char.png")
        self.index = index
    def load(self):
        super().load()
        self.subsurface(self.index)
        self.surface = pygame.transform.scale(self.surface,[16,16])
        
class Encounter(Agent):
    def __init__(self,chars):
        super().__init__()
        self.chars = []
        x=0;y=0
        for c in chars:
            cspr = Char(c)
            cspr.pos = [x,y]
            x+=9
            y+=2
            self.chars.append(cspr)
    def draw(self,engine,offset):
        offset= [offset[0]+self.pos[0],offset[1]+self.pos[1]]
        [x.draw(engine,offset) for x in self.chars]

class MMOWorld(ClickWorld):
    def __init__(self,manager,engine,game):
        super().__init__(engine)
        self.manager = manager
        self.game = game
        self.zone = systems.Zone("Test Zone",self.game,"grass")
        self.pc = Char()
        self.pc.pos = [5*32,5*32]
        self.add(self.pc)
        self.add_encounter(Encounter([ [[56,56],[8,8]] , [[56,56],[8,8]]  ,  [[56,56],[8,8]] ]))
    def add_encounter(self,encounter):
        self.add(encounter)