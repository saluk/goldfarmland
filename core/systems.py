import random
import csv

level_values = []
with open("dat/levels.csv","r") as csvfile:
    levels = csv.DictReader(csvfile,delimiter='\t')
    for row in levels:
        level_values.append(row)
        for k in row:
            row[k] = int(row[k])
print(level_values)

class SystemStruct(object):
    def __init__(self,name):
        self.name = name
        
GAME_NAMES = ["World of Wombats","Samurai Cowboy Spaceman","Elf Blood","Marital Arts Sim"]
COMPANY_NAMES = ["Egosoft","Snowstorm","Tony Electronics","Quick Buck Entertainment"]
WORLD_NAMES=["Alpha","Beta","Delta","Greek Letter"]
ACCOUNT_NAMES=["FredAstaire","GingerRogers","MrWolfe","HappyGilmore"]
LOOT_NAMES=[("Berzerker","Weapon"),("Claw","Loot"),("Mighty Helm","Helmet")]

class Company(SystemStruct):
    pass
companies = {}
for n in COMPANY_NAMES:
    companies[n] = Company(n)

class World(SystemStruct):
    def __init__(self,name,game):
        super().__init__(name)
        self.game = game
        self.game.worlds[self.name] = self
        self.characters = {}
        
class Game(SystemStruct):
    def __init__(self,name,company,speed,memory,harddrive,worlds=WORLD_NAMES):
        super().__init__(name)
        self.company = company
        self.accounts = []   #Contains accounts that can be interacted with
        self.total_accounts = 1000   #Fake number of how many player accounts exist
        self.worlds = {}
        self.speed = speed
        self.memory = memory
        self.harddrive = harddrive
        self.init_worlds(worlds)
    def init_worlds(self,worlds):
        for name in worlds:
            self.worlds[name] = World(name,self)
    def make_account(self,name):
        account = Account(name,self)
        self.accounts.append(account)
        self.total_accounts += 1
        return account
    def make_character(self,name,account,world_name):
        assert account in self.accounts
        char = AccountCharacter(name,account,self.worlds[world_name])
        return char
games = []
for n in GAME_NAMES:
    company = companies[random.choice(COMPANY_NAMES)]
    games.append(Game(n,company,random.randint(5,10),random.randint(5,10),random.randint(5,10)))

class Zone(SystemStruct):
    def __init__(self,name,game,tileset):
        super().__init__(name)
        self.game = game
        self.tileset = tileset
class FieldZone(Zone):
    def __init__(self,name,game,tileset,mobs=[]):
        super().__init__(name,game,tileset)
        self.mobs = mobs
class TownZone(Zone):
    def __init__(self,name,game,tileset,stores=[]):
        super().__init__(name,game,tileset)
        self.stores = stores
        
    
class Computer(SystemStruct):
    def __init__(self,speed,memory,harddrive):
        super().__init__("computer%s"%id(self))
        self.speed = speed
        self.memory = memory
        self.harddrive = harddrive
        self.hd_free = self.harddrive
        self.games = []
        self.running = []
    def install_game(self,game):
        if self.hd_free >= game.harddrive:
            self.games.append(game)
            self.hd_free -= game.harddrive
            return "installed"
        return "full"
    def uninstall_game(self,game):
        if game in self.games:
            self.games.remove(game)
            self.hd_free+=game.harddrive
            return "uninstalled"
        return "not installed"
    def upgrade_harddrive(self,amount):
        self.harddrive += amount
        self.hd_free += amount
    
class Account(SystemStruct):
    def __init__(self,name,game):
        super().__init__(name)
        self.game = game
        self.characters = {}
        self.banned = False
        
class Item(SystemStruct):
    def __init__(self,name,type,value):
        super().__init__(name)
        self.type = type
        self.value = value
        
class Character(SystemStruct):
    def __init__(self,name,level,maxhp,power):
        super().__init__(name)
        self.level = level
        self.maxhp = maxhp
        self.power = power
        self.gold = 0
        self.loot = []
        self.exp = 0
        self.reset()
    def reset(self):
        self.curhp = self.maxhp
    def give_exp(self,amt):
        self.exp+=amt
        while 1:
            nextlevel = self.level+1
            if len(level_values)<nextlevel:
                print("MAX LEVEL REACHED")
                return
            nextlevel = level_values[nextlevel-1]
            print(self.exp,nextlevel["exp"])
            if self.exp<nextlevel["exp"]:
                print("NOT ENOUGH EXP TO LEVEL")
                return
            self.level += 1
            self.power = nextlevel["power"]
            self.maxhp = nextlevel["hp"]
            self.reset()
            print("LEVEL UP!")
    def do_damage(self,amt):
        print(self.curhp,amt)
        self.curhp-=amt
        print(self.curhp,amt)
        if self.curhp<=0:
            self.curhp = 0
            return
        return True
    def heal(self,amt):
        self.curhp+=amt
        if self.curhp>self.maxhp:
            self.curhp = self.maxhp
            return True
    def get_loot(self,otherchar):
        name,type = random.choice(LOOT_NAMES)
        loot = Item(name,type,random.randint(1,10))
        gp = random.randint(0,10)
        self.gold += gp
        self.loot.append(loot)
        return loot,gp
            
class AccountCharacter(Character):
    def __init__(self,name,account,world):
        super().__init__(name,1,10,1)
        self.account = account
        self.account.characters[self.name] = self
        self.world = world
        self.world.characters[self.name] = self

game1 = Game(GAME_NAMES[0],COMPANY_NAMES[1],10,10,10)
World(WORLD_NAMES[0],game1)
World(WORLD_NAMES[1],game1)

computer1 = Computer(10,10,10)
print(computer1.install_game(game1))
print(computer1.install_game(game1))
computer1.upgrade_harddrive(10)
print(computer1.install_game(game1))
account1 = game1.make_account("Saluk")
account2 = game1.make_account("Xmore")
print(account1.game.name)
print(account1.characters)
char = game1.make_character("Hurtzalot",account1,"Alpha")
print(game1.worlds["Alpha"].characters)
print(char.power)
char.give_exp(9)
assert char.power==1
char.give_exp(1)
assert char.power==2
assert char.level==2