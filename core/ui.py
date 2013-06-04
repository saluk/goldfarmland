import math,random

import pygame

from .agents import Agent,Text

class Textbox(Agent):
    def init(self):
        self.font = "chaucer"
        self.lines = [Text(),Text(),Text()]
        self.text = self.lines[0]
        for l in self.lines:
            l.color = [255,255,255]
            l.font = self.font
        self.said = ""
        self.to_say = "   "
        self.layer = 11
        self.finished = False
        self.do_next = None
        self.subjects = []
        self.responses = {}
    def update(self,world):
        #Make first subject have speaking animation
        for s in self.subjects:
            s.speaking_anim = True
            break
        self.pos = [0,175]
        y = self.pos[1]+4
        for t in self.lines:
            t.pos = [self.pos[0]+4,y]
            y+=16
        if len(self.said)<len(self.to_say):
            self.said = self.to_say[:len(self.said)+1]
            self.text.set_text(self.said)
            self.text.render(world.engine)
            if self.text.surface.get_width()>314:
                words = self.said.split(" ")
                self.text.set_text(" ".join(words[:-1]))
                self.text = self.lines[self.lines.index(self.text)+1]
                self.to_say = words[-1]+self.to_say[len(self.said):]
                self.said = ""
        else:
            #No more dialog
            for s in self.subjects:
                s.speaking_anim = False
                s.speaking_offset = [0,0]
            self.finished = True
    def draw(self,engine,offset=[0,0]):
        r = pygame.Rect([self.pos[0]+1,self.pos[1]+1],[317,60])
        color = [255,255,255]
        pygame.draw.rect(engine.surface,[50,50,50],r)
        pygame.draw.rect(engine.surface,color,r,2)
        for t in self.lines:
            t.draw(engine)
    def enter(self):
        if self.do_next:
            self.do_next[0](*self.do_next[1])
    def rect(self):
        return pygame.Rect([self.pos,[320,60]])
    def click(self,world,controller):
        self.end(world)
    def end(self,world):
        for s in self.subjects:
            s.speaking = False
        world.remove(self)
        world.player.texter = None
        self.enter()
        if self.responses:
            self.responses["char"].respond(self.responses["responses"],self.responses["subjects"])

class PopupText(Text):
    def init(self):
        super(PopupText,self).init()
        self.timeout = 90
        self.layer = 11
        self.focus = None
        self.amt = 0
    def update(self,world):
        super(PopupText,self).update(world)
        self.timeout -= 1
        self.amt+=1
        self.pos = self.focus.pos[:]
        self.pos[1]-=self.amt
        if self.timeout<0:
            self.kill = 1

class Button(Agent):
    def __init__(self,graphic,target=None,func=None):
        super().__init__(graphic)
        if not target:
            target = self
        self.target = target
        self.func = func
        print(self.target,self.func)
    def event_click(self):
        func = getattr(self.target,self.func)
        func()
    def click(self):
        print(id(self),"clicked")