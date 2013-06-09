#
# a starting sprite type class
# *lazy loading
# *position, rotation
# * returns a rect that can be used for collision
# 
# a = Agent(art="path/to/image") to create
# a.pos = [150,50] to set position
# a.rot = [-1,0] to set direction vector
# image is drawn by the world, if image not yet loaded it is loaded
# multiple agents with the same image will only load the image once
#
# centered on agent.hotspot, default is [0,0] for upper left corner
# change to modify the hotspot, such as putting it in the center if you want to

import pygame
import math
import random

memory = {}
class Agent(object):
    def __init__(self,art=None,pos=None,rot=None):
        self.name = "tempname"
        self.description = "tempdesc"
        
        if not pos:
            pos = [0,0]
        if not rot:
            rot = [1,0]
        self.graphics = None
        self.surface = None
        self.pos = pos
        self.rot = rot
        self.art = art
        self.hotspot = [0,0]
        self.rotation_on_rot = False
        self.visible = True
        self.gfd = {}
        self.gft = {}
        self.layer = 2
        self.kill = 0
        self.init()
    def get_sprites(self):
        return [self]
    def init(self):
        pass
    def load(self,art=None):
        if not art:
            art = self.art
        if not art in memory:
            memory[art] = pygame.image.load(art).convert_alpha()
        self.graphics = memory[art]
        self.surface = self.graphics
        return self
    def subsurface(self,rect):
        if not self.graphics and self.art:
            self.load()
        self.surface = self.graphics.subsurface(rect)
    def update(self,world):
        if self.rotation_on_rot and self.surface:
            ang = math.atan2(-self.rot[1],self.rot[0])*180.0/math.pi
            self.surface = pygame.transform.rotate(self.graphics,ang)
    def draw(self,engine,offset=[0,0]):
        if not self.surface and self.art:
            self.load()
        if self.visible and self.surface:
            engine.surface.blit(self.surface,[self.pos[0]-self.hotspot[0]-offset[0],self.pos[1]-self.hotspot[1]-offset[1]])
    def rect(self):
        if not self.surface:
            return pygame.Rect([[0,0],[0,0]])
        r = self.surface.get_rect()
        r = r.move(self.pos[0]-self.hotspot[0],self.pos[1]-self.hotspot[1])
        return r
    def collide(self,agent,flags=None):
        """How to collide with another agent (usually the player)"""
        return
    def distance(self,agent):
        return math.sqrt((agent.pos[0]-self.pos[0])**2+(agent.pos[1]-self.pos[1])**2)
    def ai(self):
        pass
        
class Text(Agent):
    font = "font"
    def init(self):
        self.surface = None
        self.color = [0,255,0]
        self.text = ""
    def set_text(self,text,color=None):
        if color:
            self.color = color
        self.text = text
        self.surface = None
        return self
    def render(self,engine,use_bold=True):
        if not self.surface:
            bold = ""
            lastc = None
            w = 0
            h = 0
            chars = []
            for c in self.text:
                if use_bold:
                    if c=="*" and lastc==" " and not bold:
                        bold = "bold"
                        lastc = c
                        continue
                    if c=="*" and lastc!=" " and bold:
                        bold = ""
                        lastc = c
                        continue
                lastc = c
                char = getattr(engine,self.font+bold).render(c,1,self.color)
                m = getattr(engine,self.font+bold).metrics(c)
                if char.get_height()>h:
                    h = char.get_height()
                w += m[0][4]
                chars.append((char,m[0][4]))
            self.surface = pygame.Surface([w,h]).convert_alpha()
            self.surface.fill([0,0,0,0])
            x = 0
            for (char,w) in chars:
                self.surface.blit(char,[x,0])
                x+=w
    def draw(self,engine,offset=[0,0]):
        if not self.surface:
            self.render(engine)
        super(Text,self).draw(engine,offset)