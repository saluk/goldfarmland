class SystemStruct(object):
    def __init__(self,name):
        self.name = name
        
GAME_NAMES = ["World of Wombats","Samurai Cowboy Spaceman","Elf Blood","Marital Arts Sim"]
COMPANY_NAMES = ["Egosoft","Snowstorm","Tony Electronics","Quick Buck Entertainment"]
WORLD_NAMES=["Alpha","Beta","Delta","Greek Letter"]
ACCOUNT_NAMES=["FredAstaire","GingerRogers","MrWolfe","HappyGilmore"]

class Company(SystemStruct):
    pass

class Game(SystemStruct):
    def __init__(self,name,company,speed,memory,harddrive):
        super().__init__(name)
        self.company = company
        self.accounts = []   #Contains accounts that can be interacted with
        self.total_accounts = 1000   #Fake number of how many player accounts exist
        self.worlds = {}
        self.speed = speed
        self.memory = memory
        self.harddrive = harddrive
    def make_account(self,name):
        account = Account(name,self)
        self.accounts.append(account)
        self.total_accounts += 1
        return account
    def make_character(self,name,account,world_name):
        assert account in self.accounts
        char = Character(name,account,self.worlds[world_name])
        return char
    
class World(SystemStruct):
    def __init__(self,name,game):
        super().__init__(name)
        self.game = game
        self.game.worlds[self.name] = self
        self.characters = {}
    
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
    
class Character(SystemStruct):
    def __init__(self,name,account,world):
        super().__init__(name)
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
game1.make_character("Hurtzalot",account1,"Alpha")
print(game1.worlds["Alpha"].characters)