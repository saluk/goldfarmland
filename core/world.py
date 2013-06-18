#
# world.py
# a simple container of sprites, which are all rendered in order each frame
# subclass for your own scenes to actually do things

import pygame
import random
import os
import time
from .agents import Agent

class World(object):
    def __init__(self,engine):
        self.engine = engine
        self.objects = []
        self.sprites = []
        self.offset = [0,0]    #Offset for rendering
        self.control_targets = []
        self.start()
    def add(self,o):
        """Add an object to the scene"""
        self.objects.append(o)
        o.world = self
    def remove(self,o):
        self.objects.remove(o)
    def clear(self):
        self.objects[:] = []
    def start(self):
        """Code that runs when a world starts, base world
        doesn't need to do anything"""
    def update(self):
        """self.sprites starts empty, any object added to the list during
        update() is going to be rendered"""
        self.sprites = []
        for o in self.objects:
            o.update(self)
        self.objects = [o for o in self.objects if not o.kill]
        for o in self.objects:
            if o.visible:
                self.sprites.extend(o.get_sprites())
        self.sprites.sort(key=lambda sprite:(sprite.layer,sprite.pos[1]))
    def draw(self):
        """Iterate sprites and draw them"""
        [s.draw(self.engine,self.offset) for s in self.sprites]
    def input(self,controller):
        """As controller gets functions to check the state of things, input
        can be put here"""
        [x.input(controller) for x in self.control_targets]
        
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
        super().input(controller)
        
class ManagerWorld(World):
    """A world to contain other worlds and show/process one of them"""
    def __init__(self,engine):
        super().__init__(engine)
        self.worlds = [] #world[0] is current world
    def update(self):
        if self.worlds:
            self.worlds[0].update()
    def draw(self):
        if self.worlds:
            self.worlds[0].draw()
    def input(self,controller):
        if self.worlds:
            self.worlds[0].input(controller)
    def set_world(self,world):
        self.worlds = [world]
    def overlay_world(self,world):
        self.worlds.insert(0,world)
    def next_world(self,world):
        self.worlds.append(world)
    def end_current_world(self):
        del self.worlds[0]
    def end_world(self,world):
        if world in self.worlds:
            self.worlds.remove(world)