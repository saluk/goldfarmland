import pygame
import random
import math

from .agents import Agent
from .particle import Particles
from . import items
from .ui import Textbox,PopupText
from .aicontroller import AIController
from . import interactions
import re

class Player(Agent):
    def init(self):
        self.hotspot = [16,38]
        self.facing = [-1,0]
        self.next_frame = 10
        self.animdelay = 5
        self.frame = 0
        self.anim = None
        self.animating = False
        self.walk_speed = 0.5
        self.vector = [0,0]
        self.mood = "happy"
        self.speaking = False
        self.speaking_anim = False
        self.speaking_offset = [0,0]
        
        self.particles = Particles()
        
        self.radius = 14   #collision radius around hotspot
        
        self.last_hit = None
        
        self.moved = False
        self.following = None
        self.follow_path = ""
        
        self.last_random_point = None
        self.next_random_point = 0
        
        self.items = items.Inventory()
        names = items.Item.names[:]
        for i in range(random.randint(1,4)):
            name = random.choice(names)
            names.remove(name)
            self.items.add(name=name)
        
        self.menu = None
        self.texter = None
        
        self.aicontroller = AIController(self)
        self.interactable = interactions.CharacterInteractable(self)
        self.quests = []
        
        self.topics = set([])
    def click(self,world,controller):
        if self.name=="erik":
            self.mymenu()
        else:
            self.action()
    def get_map(self):
        return self.world.maps[self.mapname]
    def get_path(self,pathname,get_astar=False):
        if pathname==True:
            return
        map = self.get_map()
        if pathname not in map.paths:
            return
        path = map.paths[pathname][:]
        if get_astar:
            path = self.update_path(path)
        return path
    def update_path(self,path):
        print("update path",len(path),path)
        if not path:
            return None
        map = self.get_map()
        map.remove_entity(self)
        map.reset_astar_graph()
        path2 = []
        #Get open tiles around our tile
        tx,ty = self.pos[0]//32,self.pos[1]//32
        open_tiles = []
        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                if not map.is_blocked((tx+dx,ty+dy)):
                    open_tiles.append(((tx+dx)*32,(ty+dy)*32))
        next = path[0]
        if path[1:]:
            next = path[1]
        open_tiles.sort(key=lambda p:((next[0]-p[0]**2)+(next[1]-p[1]**2)))
        if not open_tiles:
            return None
        p = open_tiles[0]
        path2.extend(map.get_path(p,path[0]))
        if not path2:
            return self.update_path(path[1:])
        for i,next in enumerate(path[1:]):
            if path2[-1]==next:
                continue
            np = map.get_path(path2[-1],next)
            if np:
                for p in np:
                    if p!=path2[-1]:
                        path2.append(p)
            else:
                return None
                rest = path[i+1:]
                if not rest:
                    return None
                print(i)
                print(path)
                if i>0:
                    path = path2+path[i+1:]
                else:
                    path = path[i+1:]
                print(path)
                print("uh oh. no path found, try to path to the next starting point")
                return self.update_path(path)
        map.add_entity(self)
        return path2
    def assign_ai(self,active=True):
        self.aicontroller.active = active
    def ai(self):
        if self.aicontroller.active:
            self.aicontroller.control()
    def load(self,spritesheet):
        super(Player,self).load(spritesheet)
        self.anims = {}
        order = ["down","left","right","up"]
        for y in range(4):
            frames = []
            for x in range(4):
                frames.append(self.graphics.subsurface([[x*32,y*48],[32,48]]))
            self.anims[order[y]] = frames
    def draw(self,engine,offset=[0,0]):
        elipserect = [[0,0],[20,12]]
        elipse = pygame.Surface([20,12]).convert_alpha()
        elipse.fill([0,0,0,0])
        pygame.draw.ellipse(elipse,[0,0,0,50],elipserect)
        self.particles.draw(engine,offset)
        engine.surface.blit(elipse,[self.pos[0]-offset[0]-10,self.pos[1]-offset[1]])
        p = self.pos[:]
        self.pos[1]-=self.speaking_offset[0]
        super(Player,self).draw(engine,offset)
        self.pos = p
        x,y = (self.pos[0])//32*32-offset[0],(self.pos[1])//32*32-offset[1]
        w,h = 32,32
        #pygame.draw.rect(engine.surface,[255,0,255],pygame.Rect([[x,y],[w,h]]))
        for p in self.aicontroller.following_points:
            pygame.draw.rect(engine.surface,[255,0,255],[[p[0]-offset[0],p[1]-offset[1]],[2,2]])
        #engine.surface.blit(engine.font.render(self.aicontroller.state,1,[255,0,0]),[self.pos[0]-offset[0],self.pos[1]-offset[1]])
    def walk(self):
        self.map.remove_entity(self)
        
        self.moved = False
        col1=col2=None
        
        #calculate inside collisions
        col0 = self.world.collide(self)
        
        if self.vector[0]:
            self.pos[0]+=self.vector[0]*self.walk_speed
            col1 = self.world.collide(self,"move")
            if col1 and not col0:
                self.pos[0]-=self.vector[0]*self.walk_speed
            else:
                self.facing = [self.vector[0],0]
                self.moved = True
        if self.vector[1]:
            self.pos[1]+=self.vector[1]*self.walk_speed
            col2 = self.world.collide(self,"move")
            if col2 and not col0:
                self.pos[1]-=self.vector[1]*self.walk_speed
            else:
                self.facing = [0,self.vector[1]]
                self.moved = True
        
        hit_any = None
        for col in col1,col2:
            if col:
                hit_any = col
                if isinstance(col,dict):
                    if "warptarget" in col:
                        self.world.change_map(self,col["map"],col["warptarget"])
                        
        if hit_any:
            self.last_hit = hit_any
        else:
            self.last_hit = None
        
        if self.moved:
            self.animating = True
            self.particles.active = True
            self.particles.vector = [-self.vector[0],-self.vector[1]]
            
        self.map.add_entity(self)
    def say(self,text,actor=None,subjects=[]):
        if self.name != "erik":
            return
        for s in subjects:
            s.speaking = True
        if not actor:
            actor = self
        self = actor
        self.texter = Textbox()
        self.texter.subjects = subjects
        responses = re.findall("\{.*?\}",text)
        for r in responses:
            text = text.replace(r,"")
        print(responses)
        self.texter.to_say = text
        if responses:
            self.texter.responses = {"char":self,"subjects":subjects,"responses":[x[1:-1].split(",") for x in responses]}
        self.world.add(self.texter)
        topics = text.split("*")
        in_topic = False
        for i,t in enumerate(topics):
            if in_topic:
                self.topics.add(t)
            in_topic = not in_topic
            print(self.topics)
        print(self.texter,self.texter.to_say,self.texter.said,self.texter.pos)
    def respond(self,responses,subjects):
        """Allow player to choose something to say to the subjects"""
        options = []
        for r in responses:
            options.append( (r[0],subjects[0].interactable.action_dialog,(self,r[1])) )
        self.menu.setup(options,label="Respond")
    def say_many(self,lines,actor=None,subjects=[]):
        self = actor
        self.say(lines[0],actor,subjects)
        if lines[1:]:
            self.texter.do_next = (self.say_many,(lines[1:],actor,subjects))
    def frobme(self,actor):
        self.interactable.frobme(actor)
    def mymenu(self):
        if not self.menu:
            return
        options = []
        if self.items:
            options.append( ("items[%d]"%self.items.length(),self.show_items,(self,None)) )
        self.menu.setup(options,label="Character Menu")
    def show_items(self,actor,item):
        if not self.menu:
            returrn
        options = []
        for i in self.items:
            options.append( (i.name,self.examine_item,(self,i)) )
        self.menu.setup(options,label="Items")
    def examine_item(self,actor,item):
        self.say(item.description)
    def follow(self,actor):
        self.following = actor
        #self.world.camera_focus = self
    def unfollow(self,actor):
        self.following = None
        self.following_points = []
        #self.world.camera_focus = actor
    def action(self):
        """Interact with object in front of us"""
        p = self.pos[:]
        for s in range(3):
            p[0]+=self.facing[0]*8
            p[1]+=self.facing[1]*8
            col = self.world.collide_point(self,p,"frobme")
            if col:
                print(col,dir(col))
                if hasattr(col,"frobme"):
                    col.frobme(self)
                return
    def idle(self):
        self.animating = False
        self.particles.active = False
        self.vector = [0,0]
    def forward(self):
        self.vector[:] = self.facing[:]
    def left(self):
        self.facing = [-1,0]
        self.vector[0] = -1
    def right(self):
        self.facing = [1,0]
        self.vector[0] = 1
    def up(self):
        self.facing = [0,-1]
        self.vector[1] = -1
    def down(self):
        self.facing = [0,1]
        self.vector[1] = 1
    def set_anim(self,anim):
        self.anim = anim
        self.frame = 0
        self.next_frame = self.animdelay
        self.set_animation_frame()
    def set_animation_frame(self):
        anim = self.anims[self.anim]
        if self.frame>=len(anim):
            self.frame = 0
        self.surface = anim[self.frame]
    def update(self,world):
        if self.vector[0] or self.vector[1]:
            self.walk()
            
        if self.facing[0]<0:
            anim = "left"
        elif self.facing[0]>0:
            anim = "right"
        elif self.facing[1]<0:
            anim = "up"
        elif self.facing[1]>0:
            anim = "down"
        else:
            anim = self.anim
        if anim!=self.anim:
            self.set_anim(anim)
        if self.animating:
            self.next_frame -= 1
        if self.next_frame<=0:
            self.next_frame = self.animdelay
            self.frame += 1
            self.set_animation_frame()
        
        self.particles.pos = self.pos[:]
        self.particles.update(world)
        
        if self.speaking_anim:
            self.speaking_offset[0] = 2+math.sin(self.speaking_offset[1])*2
            self.speaking_offset[1]+=0.5
        
        
    def collide(self,agent,flags=None):
        return self.collide_point(agent.pos,flags)
    def collide_point(self,p,flags=None):
        radius = self.radius
        #sp = [x//32*32 for x in self.pos]
        #left,top,right,bottom = sp[0],sp[1],sp[0]+32,sp[1]+32
        left,top,right,bottom = self.pos[0]-radius,self.pos[1]-radius,self.pos[0]+radius,self.pos[1]+radius
        if p[0]>=left and p[0]<=right and p[1]>=top and p[1]<=bottom:
            return self
    def rect(self):
        radius = self.radius
        left,top,right,bottom = self.pos[0]-radius+1,self.pos[1]-radius+1,self.pos[0]+radius-1,self.pos[1]+radius-1
        return pygame.Rect([[left,top],[right-left,bottom-top]])
