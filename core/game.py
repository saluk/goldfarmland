import os,random,math

import pygame

from world import World

from agents import Text,Agent

import json

class LogoWorld(World):
    def start(self):
        self.add(Agent("art/icons/logo.png"))

class GameWorld(World):
    def start(self):
        self.objects = []
    def update(self):
        self.sprites = []
        for o in self.objects:
            o.update(self)
        self.objects = [o for o in self.objects if not o.kill]
        for o in self.objects:
            if o.visible:
                self.sprites.extend(o.get_sprites())
    def input(self,controller):
        if controller.restart:
            import game
            import world
            reload(world)
            reload(game)
            self.engine.world = game.make_world(self.engine)
            return
        if controller.mbdown:
            x = controller.mpos[0]+self.offset[0]
            y = controller.mpos[1]+self.offset[1]
            for o in reversed(self.sprites):
                r = o.rect()
                if hasattr(o,"click") and x>=r.left and x<=r.right and y>=r.top and y<=r.bottom:
                    o.click(self,controller)
                    return
        if controller.quit:
            self.engine.running = False

def make_world(engine):
    """This makes the starting world"""
    w1 = LogoWorld(engine)
    w = GameWorld(engine)
    return w1