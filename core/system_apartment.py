from .world import World,ClickWorld
from .agents import Agent
from .ui import Button
from . import system_computer

class ApartmentWorld(ClickWorld):
    def __init__(self,computer,manager,engine):
        super().__init__(engine)
        self.computer = computer
        self.manager = manager
        self.add(Agent("art/gui/apartment_screen.png"))
        comp = Button("art/gui/apt_computer.png",{"func":self.run_computer})
        comp.pos = [76,124]
        self.add(comp)
    def run_computer(self):
        self.manager.overlay_world(system_computer.ComputerWorld(self.manager,self.engine,self.computer))