import pygame
import math
from src.debuff import SlowDebuff,PoisonDebuff
DEFAULT_IMAGE_SIZE = (40, 40)
class plot:
    def __init__(self, x, y,texture,defaultplant,board):
        self.positionx = (x)
        self.positiony = (y)
        self.texture = texture
        self.plant = defaultplant
        self.type = "plot"
        self.board = board
    def checkpos(self):
        return self.positionx , self.positiony
    def checkplant(self):
        return self.plant
    def draw(self):
        c = 120+60*self.positionx
        v = 100+60*self.positiony
        self.board.give_screen().blit(self.texture,(c,v))
        if self.plant != self.board.return_default():
            plantedimgs = self.plant.giveimg()
            DEFAULT_IMAGE_SIZE = (50, 50)
            slotimgs = pygame.transform.scale(plantedimgs, DEFAULT_IMAGE_SIZE)
            self.board.give_screen().blit(slotimgs,(c+5,v+5))
    def change_texture(self,newtexture):
        self.texture = newtexture
    def checkclick(self,x,y):
        return self.positionx == x and self.positiony == y
    def planted(self):
        return self.plant == self.board.return_default()
    def planting(self,plant,cost):
        if self.plant == self.board.return_default() and self.type == "plot":
            self.plant = plant
            self.board.update_sun(-cost)
            self.board.addplant(self.plant)
            x = self.positionx*60+120
            y = self.positiony*60+100
            self.plant.location(x,y)

    def change_type(self,newplot):
        self.type= newplot
    def givetype(self):
        return self.type
    def givexy(self):
        return [self.positionx,self.positiony]
    


class slot:
    def __init__(self,plant,x,y,board):
        self.plant = plant
        self.posx = x
        self.posy = y
        self.board = board
    def display(self):
        slotimgs = self.plant.giveimg()
        DEFAULT_IMAGE_SIZE = (80, 90)
        slotimgs = pygame.transform.scale(slotimgs, DEFAULT_IMAGE_SIZE)
        self.board.give_screen().blit(slotimgs,(self.posx,self.posy))
    def ifclicked(self,x,y):
        xstuff = x-self.posx
        ystuff = y-self.posy
        if self.plant.cost <= self.board.give_sun():
            return xstuff <80 and xstuff >0 and ystuff <90 and ystuff >0
    def display1(self,x,y):
        slotimgs = self.plant.giveimg()
        DEFAULT_IMAGE_SIZE = (80, 90)
        slotimgs = pygame.transform.scale(slotimgs, DEFAULT_IMAGE_SIZE)
        self.board.give_screen().blit(slotimgs,(x,y))
    def getprice(self):
        return self.plant.giveprice()
        
class board:
    def __init__(self,screen,default):
        self.screen = screen
        self.plots = []
        self.sunlight = 200
        self.playerhealth = 10
        self.action_list = []
        self.entity_to_display = []
        self.enemy_list = []
        self.projectile_list =[]
        self.default_plant=default
    def plantings(self,x,y,plant,price):
        for i in self.plots:
            if i.checkclick(x,y) and i.planted():
                i.planting(plant,price)
    def clickeditem(self,x,y):
        for i in self.entity_to_display:
            if i.ifclicked(x,y):
                return i
        return False
    def give_playerhealth(self):
        return self.playerhealth
    def give_plots(self):
        return self.plots
    def add_entity(self,entity):
        self.entity_to_display.append(entity)
    def give_entity(self):
        return self.entity_to_display
    def return_default(self):
        return self.default_plant
    def createboard(self):
        tile_image = pygame.image.load("./resource/tiles.png")
        tile_image = pygame.transform.scale(tile_image,(60,60))
        for i in range(15):
            for a in range(9):
                self.plots.append(plot(i,a,tile_image,self.default_plant,self))
    def update_sun(self,number):
        self.sunlight += number
    def give_sun(self):
        return self.sunlight
    def loosehp(self):
        self.playerhealth = self.playerhealth-1
    def addplant(self,plant):
        self.action_list.append(plant)
    def add_enemy(self,enemy):
        self.enemy_list.append(enemy)
    def add_projectile(self,projectile):
        self.projectile_list.append(projectile)
    def give_enemy(self):
        return self.enemy_list
    def drawboard(self):
      for i in self.plots:
        i.draw()
    def changegrid(self,x,y,type,texture):
        self.plots[x*9+y].change_type(type)
        self.plots[x*9+y].change_texture(texture)
    def allentity(self):
        def remove_death(thelist):
            deadlist = []
            count = 0
            for i in thelist:
                if i.hp <= 0:
                    deadlist.append(count)
                count += 1
            for i in range(len(deadlist)):
                thelist.pop(deadlist[-1])
                deadlist.pop(-1)
            return thelist
        for i in self.action_list:
            actions(i)
        self.action_list = remove_death(self.action_list)
        for i in self.enemy_list:
            i.action()
        self.enemy_list = remove_death(self.enemy_list)
        for i in self.projectile_list:
            i.action()
        self.projectile_list = remove_death(self.projectile_list)
    def give_screen(self):
         return self.screen
def actions(object):
    object.timeuntilaction -= 0.1
    if object.timeuntilaction <= 0:
        object.action()
        object.timeuntilaction = object.time
class projectile:
    def __init__(self,dmg,target,location,board):
        self.dmg = dmg
        self.target = target
        self.targetxy = target.xypos()
        self.location = location
        self.hp = 1
        self.img = pygame.image.load("./resource/projectile.png")
        self.board = board
    def updatetarget(self):
        self.targetxy = self.target.xypos()
        if self.target.hp <= 0:
            self.hp = 0
    def action(self):
        self.updatetarget()
        enemy_list = self.board.give_enemy()
        boom = self.search(enemy_list)
        if boom != False:
            boom.loosehp(self.dmg)
            self.hp =0 
        else:
            a = (-self.location[0] + self.targetxy[0])
            b = (-self.location[1] + self.targetxy[1])
            xmove = 0
            ymove = 0
            moved = 0
            if b>0:
                var = 1
                b += 1
            else:
                var = -1
                b+= -1
            ratio = a/b
            while moved < 3:
                ymove +=var
                xmove +=int(round(ratio*var))
                moved = math.sqrt(ymove**2+xmove**2)
            
            self.location[0] += round(xmove)
            self.location[1]+= round(ymove)
            self.display()
    def display(self):
        enemyimg = self.img
        DEFAULT_IMAGE_SIZE = (10, 10)
        enemyimg = pygame.transform.scale(enemyimg, DEFAULT_IMAGE_SIZE)
        self.board.give_screen().blit(enemyimg,self.location)
                    
    def search(self,enemy):
        for i in enemy:
            temp = i.xypos()
            x = temp[0]
            y = temp[1]
            if x> self.location[0] -20 and x < self.location[0]+20 and y> self.location[1] -20 and y< self.location[1] + 20:
                return i
        return False
class projectile_slow(projectile):
    def __init__(self, dmg, target, location, board):
        super().__init__(dmg, target, location, board)
        self.img = pygame.image.load("./resource/slow_project.png")
    def action(self):
            self.updatetarget()
            enemy_list = self.board.give_enemy()
            boom = self.search(enemy_list)
            if boom != False:
                boom.loosehp(self.dmg)
                boom.add_debuff(SlowDebuff(500,boom))
                self.hp =0 
            else:
                a = (-self.location[0] + self.targetxy[0])
                b = (-self.location[1] + self.targetxy[1])
                xmove = 0
                ymove = 0
                moved = 0
                if b>0:
                    var = 1
                    b += 1
                else:
                    var = -1
                    b+= -1
                ratio = a/b
                while moved < 3:
                    ymove +=var
                    xmove +=int(round(ratio*var))
                    moved = math.sqrt(ymove**2+xmove**2)
                self.location[0] += round(xmove)
                self.location[1]+= round(ymove)
                self.display()

class projectile_poison(projectile):
    def __init__(self, dmg, target, location, board):
        super().__init__(dmg, target, location, board)
        self.img = pygame.image.load("./resource/poison_proj.png")
    def action(self):
            self.updatetarget()
            enemy_list = self.board.give_enemy()
            boom = self.search(enemy_list)
            if boom != False:
                boom.loosehp(self.dmg)
                boom.add_debuff(PoisonDebuff(500,boom))
                self.hp =0 
            else:
                a = (-self.location[0] + self.targetxy[0])
                b = (-self.location[1] + self.targetxy[1])
                xmove = 0
                ymove = 0
                moved = 0
                if b>0:
                    var = 1
                    b += 1
                else:
                    var = -1
                    b+= -1
                ratio = a/b
                while moved < 3:
                    ymove +=var
                    xmove +=int(round(ratio*var))
                    moved = math.sqrt(ymove**2+xmove**2)
                self.location[0] += round(xmove)
                self.location[1]+= round(ymove)
                self.display()
