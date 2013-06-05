from . import systems
from .world import World,ClickWorld
from .ui import Button
from .agents import Agent

class ComputerWorld(ClickWorld):
    def __init__(self,engine,computer):
        super().__init__(engine)
        self.computer = computer
        self.add(Agent("art/gui/comp_screen.png"))