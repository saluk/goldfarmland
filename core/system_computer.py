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
        self.add(TextButton(box=pygame.Rect([0,0],[40,20]),text="Quit",pos=[240,180],target=self,func="action_quit"))
    def action_quit(self):
        print("ending world")
        self.manager.end_world(self)