import random
import pygame
import json

from . import systems
from . import m
from .world import World,ClickWorld
from .ui import Button,TextButton
from .agents import Agent

mob_defs = json.load(open("dat/mobs.json"))

class Char(Agent):
    def __init__(self,sprite_name):
        super().__init__("art/sprites/char.png")
        self.chars = [self]
        self.index = mob_defs["sprites"][sprite_name]["rect"]
        self.hp = 10
        self.power = 1      #hp per loss per attack
    def load(self):
        super().load()
        self.subsurface(self.index)
        self.surface = pygame.transform.scale(self.surface,[16,16])
    def collide(self,agent,flags=None):
        return self.rect().colliderect(agent.rect())
    def draw(self,engine,offset):
        super().draw(engine,offset)
        pygame.draw.line(engine.surface,[255,0,0],[self.pos[0]-offset[0],self.pos[1]-offset[1]-3],[self.pos[0]-offset[0]+int(32*(self.hp/10.0)),self.pos[1]-offset[1]-3])
        
class Fight(object):
    def __init__(self,partya,partyb):
        self.partya = partya
        self.partya.name = "Ghosts"
        self.partyb = partyb
        self.partyb.name = "Hurtzalot"
        self.turns = [self.partya,self.partyb]
        self.time_per_attack = 10
        self.next_attack = 0
        self.winner = None
    def update(self):
        self.next_attack += 1
        if self.next_attack>=self.time_per_attack:
            self.next_attack = 0
            self.take_turn()
    def take_turn(self):
        attacker = self.turns[0]
        defender = self.turns[1]
        self.turns = [defender,attacker]
        for char in attacker.chars:
            defender.chars[0].hp -= char.power
            print(defender.chars[0].name+" takes %s"%char.power+" damage")
            if defender.chars[0].hp<=0:
                del defender.chars[0]
                if not defender.chars:
                    break
        if not defender.chars:
            print(defender.name+" has lost")
            self.winner = attacker
        
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
            cspr.hp = 1
            cspr.name = "Ghost"
            x+=9
            y+=2
            self.chars.append(cspr)
            self.rh = y+cspr.rect().height
            self.rw = x+cspr.rect().width
        self.fight = None
    def rect(self):
        return pygame.Rect([self.pos,[self.rw,self.rh]])
    def draw(self,engine,offset):
        offset= [offset[0]-self.pos[0],offset[1]-self.pos[1]]
        [x.draw(engine,offset) for x in self.chars]

class MMOWorld(ClickWorld):
    def __init__(self,computer,manager,engine,game):
        super().__init__(engine)
        self.computer = computer
        self.manager = manager
        self.game = game
        self.zone = systems.Zone("Test Zone",self.game,"grass")
        self.pc = Char("elf_archer")
        self.pc.name = "Hurtzalot"
        self.pc.pos = [5*32,4*32]
        self.encounters = []
        self.add(self.pc)
        self.add_encounter(Encounter(0, [ "ghost_blue" ]))
        self.add_encounter(Encounter(1, [ "ghost_blue" ]))
        self.add_encounter(Encounter(2, [ "ghost_blue"  ]))
        self.add_encounter(Encounter(3, [ "ghost_blue"  ]))
        self.next_encounter = 0
        self.encounter_rate = 100
        self.next_health = 0
        self.health_rate = 50
    def add_encounter(self,encounter):
        self.add(encounter)
        self.encounters.append(encounter)
    def remove_encounter(self,encounter):
        self.remove(encounter)
        self.encounters.remove(encounter)
    def check_fights(self):
        fights = []
        for enc in self.encounters:
            if self.pc.collide(enc):
                fights.append(enc)
        return fights
    def move_encounters(self):
        for enc in self.encounters:
            dx,dy = m.toward(enc,self.pc)
            enc.pos[0]+=dx
            enc.pos[1]+=dy
        self.next_encounter += 1
        if self.next_encounter >= self.encounter_rate:
            self.next_encounter = 0
            self.add_encounter(Encounter(0, [ "ghost_blue" ]))
            self.add_encounter(Encounter(1, [ "ghost_blue" ]))
            self.add_encounter(Encounter(2, [ "ghost_blue"  ]))
            self.add_encounter(Encounter(3, [ "ghost_blue"  ]))
        self.next_health += 1
        if self.next_health >= self.health_rate:
            self.next_health = 0
            if self.pc.hp<10:
                self.pc.hp += 1
    def do_fights(self,fights):
        for enc in fights:
            if not enc.fight:
                enc.fight = Fight(enc,self.pc)
            enc.fight.update()
            break
        if fights[0].fight.winner==self.pc:
            self.remove_encounter(fights[0])
        elif fights[0].fight.winner:
            print("PLAYER DIED")
            self.manager.use_computer(self.computer)
    def update(self):
        super().update()
        fights = self.check_fights()
        if fights:
            self.do_fights(fights)
        else:
            self.move_encounters()