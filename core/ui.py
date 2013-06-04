import math,random

import pygame

from .agents import Agent,Text

class Radial(Agent):
    def init(self):
        self.label = Text()
        
        self.timer = Text()
        self.ttl = -1
        
        self.options = []
        self.radius = 0
        self.target_radius = 48
        self.angle = 0
        self.diff_angle = 0
        self.pause = False
        
        self.overlay = pygame.Surface([320,240])
        self.overlay.fill([0,0,0])
        self.overlay.set_alpha(50)
        
        self.flashi = 10
    def update(self,world):
        if self.radius<self.target_radius:
            self.radius += 4
        if self.angle>0:
            self.angle-=self.diff_angle/10.0
        if self.angle<0:
            self.angle+=self.diff_angle/10.0
        if self.ttl>0:
            self.ttl-=1
        if self.ttl==0:
            self.action()
    def draw(self,engine,offset=[0,0]):
        if not self.options:
            self.visible = False
            return
        engine.surface.blit(self.overlay,[0,0])
            
        angle = 3.0*(2.0*math.pi/4.0)+float(self.angle)
        self.flashi-=1
        if self.flashi>5:
            color = [190,255,190]
        else:
            color = [50,255,50]
        if self.flashi<0:
            self.flashi = 10
        self.label.draw(engine)
        for option in self.options:
            dx,dy = self.radius*math.cos(angle),self.radius*math.sin(angle)
            center_pos = [self.pos[0]-offset[0],self.pos[1]-offset[1]]
            cp0 = center_pos[:]
            center_pos[0]+=dx
            center_pos[1]+=dy
            cp1 = center_pos[:]
            r = option.rect()
            center_pos[0]-=r.width//2
            center_pos[1]-=r.height//2
            option.pos = center_pos
            pygame.draw.line(engine.surface,[255,0,0],cp0,cp1)
            pygame.draw.rect(engine.surface,[50,50,50],option.rect().inflate(4,4))
            pygame.draw.rect(engine.surface,color,option.rect().inflate(4,4),1)
            color = [150,150,150]
            option.draw(engine)
            angle += self.diff_angle
        if self.ttl!=-1:
            self.timer.set_text("Time Left: %.02f"%(self.ttl/30.0,))
            self.timer.pos = [200,80]
            self.timer.draw(engine)
    def rotate_right(self):
        self.options.append(self.options.pop(0))
        self.angle+=self.diff_angle
    def rotate_left(self):
        self.options.insert(0,self.options.pop(-1))
        self.angle-=self.diff_angle
    def setup(self,options,pause=True,label="Test Label",ttl=-1):
        self.angle = 0
        self.radius = 0
        self.label.set_text(label)
        self.options = []
        if ttl!=-1:
            self.ttl = ttl
        for option_text,option_command,option_args in options:
            t = Text()
            t.set_text(option_text)
            t.color = [240,240,240]
            t.command = option_command
            t.args = option_args
            self.options.append(t)
        self.enable()
        self.pause = pause
        
        max_angle = 2*math.pi
        self.diff_angle = max_angle/float(len(self.options))
    def enable(self):
        self.world.engine.play_sound("mario_bounce")
        self.visible = True
    def disable(self):
        self.visible = False
    def action(self):
        self.ttl=-1
        self.disable()
        o = self.options[0]
        if hasattr(o,"command"):
            o.command(*o.args)

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