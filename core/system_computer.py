import random
import pygame

from . import systems
from .world import World,ClickWorld
from .ui import Button,TextButton
from .agents import Agent

class ComputerWorld(ClickWorld):
    def __init__(self,manager,engine,computer):
        super().__init__(engine)
        self.manager = manager
        self.computer = computer
        self.screen = "desktop"
        self.build_screen()
    def build_screen(self):
        self.clear()
        self.add(Agent("art/gui/comp_screen.png"))
        getattr(self,"build_"+self.screen)()
    def build_desktop(self):
        x = 20
        y = 20
        for game in self.computer.games:
            self.add(TextButton(box=pygame.Rect([0,0],[40,20]),text=game.name,pos=[x,y],caller={"func":self.action_launch,"game":game}))
            x+=50
            if x>300:
                x=0
                y+=20
        self.add(TextButton(box=pygame.Rect([0,0],[40,20]),text="Quit",pos=[240,180],caller={"func":self.action_quit}))
        self.add(TextButton(box=pygame.Rect([0,0],[40,20]),text="Install",pos=[200,180],caller={"func":self.action_install}))
    def action_quit(self):
        print("ending world")
        self.manager.end_world(self)
    def action_install(self,game=None):
        if not game:
            game = random.choice(systems.games)
        result = self.computer.install_game(game)
        print(result)
        self.build_screen()
    def action_launch(self,game):
        print("Starting game "+game.name)