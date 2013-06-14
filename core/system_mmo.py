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
    def collide(self,agent,flags=None):
        return self.rect().colliderect(agent.rect())
        
class Encounter(Agent):
    def __init__(self,corner,chars):
        super().__init__()
        if corner==0:
            self.pos = [0,0]
        elif corner==1:
            self.pos = [320,0]
        elif corner==2:
            self.pos = [320,240]
        elif corner==3:
            self.pos = [0,240]
        self.chars = []
        x=0;y=0
        for c in chars:
            cspr = Char(c)
            cspr.load()
            cspr.pos = [x,y]
            x+=9
            y+=2
            self.chars.append(cspr)
            self.rh = y+cspr.rect().height
            self.rw = x+cspr.rect().width
    def rect(self):
        return pygame.Rect([self.pos,[self.rw,self.rh]])
    def draw(self,engine,offset):
        offset= [offset[0]-self.pos[0],offset[1]-self.pos[1]]
        [x.draw(engine,offset) for x in self.chars]

class MMOWorld(ClickWorld):
    def __init__(self,manager,engine,game):
        super().__init__(engine)
        self.manager = manager
        self.game = game
        self.zone = systems.Zone("Test Zone",self.game,"grass")
        self.pc = Char()
        self.pc.pos = [5*32,4*32]
        self.encounters = []
        self.add(self.pc)
        self.add_encounter(Encounter(0, [ [[56,56],[8,8]] , [[56,56],[8,8]]  ,  [[56,56],[8,8]] ]))
        self.add_encounter(Encounter(1, [ [[56,56],[8,8]] , [[56,56],[8,8]]  ,  [[56,56],[8,8]] ]))
        self.add_encounter(Encounter(2, [ [[56,56],[8,8]] , [[56,56],[8,8]]  ,  [[56,56],[8,8]] ]))
        self.add_encounter(Encounter(3, [ [[56,56],[8,8]] , [[56,56],[8,8]]  ,  [[56,56],[8,8]] ]))
    def add_encounter(self,encounter):
        self.add(encounter)
        self.encounters.append(encounter)
    def check_fights(self):
        fights = []
        for enc in self.encounters:
            if self.pc.collide(enc):
                fights.append(enc)
        return fights
    def move_encounters(self):
        for enc in self.encounters:
            if enc.pos[0]<self.pc.pos[0]:
                enc.pos[0]+=1
            elif enc.pos[0]>self.pc.pos[0]+32:
                enc.pos[0]-=1
            if enc.pos[1]<self.pc.pos[1]:
                enc.pos[1]+=1
            elif enc.pos[1]>self.pc.pos[1]+32:
                enc.pos[1]-=1
    def do_fights(self,fights):
        pass
    def update(self):
        super().update()
        fights = self.check_fights()
        if fights:
            self.do_fights(fights)
        else:
            self.move_encounters()