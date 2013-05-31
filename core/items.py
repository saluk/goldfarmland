import random
import json

itemdat = json.loads(open("dat/items.json").read())
item_defs = itemdat["items"]

from agents import Agent

class Item(Agent):
    names = ["apple","bananna","handkerchief","gloves","axe","sword","bucket","ring","bracelet","knife","coins","note","booklet","glass","leaflet"]
    def init(self):
        names = Item.names[:]
        self.name = random.choice(names)
        self.description = "xxx"
    def set_values(self,name):
        self.name = name
        self.description = item_defs.get(name,{}).get("description","The item is named "+name)
    def serialized(self):
        return {"pos":self.pos,"name":self.name,"description":self.description}
    @staticmethod
    def unserialize(d):
        i = Item()
        i.pos = d["pos"]
        i.name = d["name"]
        i.description = d["description"]
        return i
        
class Inventory(Agent):
    def __init__(self):
        self.items = []
    def names(self):
        return [x.name for x in self.items]
    def clear(self):
        self.items = []
    def get(self,name=None):
        if name:
            all = [x for x in self.items if x.name==name]
            if all:
                return all[0]
    def remove(self,item=None,name=None):
        if name:
            item = self.get(name)
        if item:
            print self.names()
            self.items.remove(item)
            return item
    def add(self,item=None,name=None):
        if name:
            item = Item()
            item.set_values(name)
        self.items.append(item)
    def transfer(self,from_inventory,item=None,name=None):
        item = from_inventory.remove(item,name)
        self.add(item)
    def length(self):
        return len(self.items)
    def __iter__(self):
        return iter(self.items)