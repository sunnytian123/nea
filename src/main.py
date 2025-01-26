#todo readme graphic, python doc,comment class, change enemy.update_direction so it doesnt search everything, python enum
import pygame
import copy
import random
import math
import enemy
import mapgen
from enemy import Basic,Speed,Tank
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
        tile_image = pygame.image.load("resource/tiles.png")
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
class plant:
    def __init__(self,board):
        self.positionx = 0
        self.positiony = 0
        self.cost = 0
        self.hp = 0
        self.time = 0 
        self.growtht = 0
        self.growth = False
        self.img = 0
        self.timeuntilaction = self.time
        self.board = board
    def loosehp(self,dmg):
        self.hp +=-dmg
    def growthcheck(self):
        if not self.growth:
            self.growtht -= 1
        else:
            self.growth = True
    def giveimg(self):
        return self.img
    def giveprice(self):
        return self.cost
    def location(self,x,y):
        self.positionx = x
        self.positiony = y
        
class sunflower(plant):
    def __init__(self,board):
        super().__init__(board)
        self.img = pygame.image.load("resource/sunflower.png")
        self.cost = 100
        self.hp = 100
        self.time = 50
        self.timeuntilaction = 50
    def action(self):
        self.board.update_sun(100)
class shooter(plant):
    def __init__(self,board):
        super().__init__(board)
        self.img = pygame.image.load("resource/bow.png")
        self.cost = 100
        self.hp = 100
        self.time = 20
        self.timeuntilaction = 20
        self.dmg = 10
    def search(self,enemy):
        in_range = []
        #merge sort
        closest = False
        for i in enemy:
            temp = i.xypos()
            x = temp[0]
            y = temp[1]
            if x> self.positionx -300 and x < self.positionx+300 and y> self.positiony -300 and y< self.positiony + 300:
                in_range.append(i)
        distance = []
        for i in in_range:
            temp = i.xypos()
            x = temp[0]
            y = temp[1]
            if isinstance(x,float):
                x = int(x+0.5)
            if isinstance(y,float):
                y = int(y+0.5)
            d = float((self.positionx-x)**2) + float((self.positiony-y)**2)
            distance.append(d)
        if len(distance) > 0:
            mergeSort(distance)
            closest = distance[0]
            for i in in_range:
                temp = i.xypos()
                x = temp[0]
                y = temp[1]
                if isinstance(x,float):
                    x = int(x+0.5)
                if isinstance(y,float):
                    y = int(y+0.5)
                d = float((self.positionx-x)**2) + float((self.positiony-y)**2)
                if d == closest:
                    closest = i
        return closest
    def action(self):
        enemy_list = self.board.give_enemy()
        target = self.search(enemy_list)
        if target != False:
            self.board.add_projectile(projectile(self.dmg,target,[self.positionx,self.positiony],self.board))

class slower(shooter):
    def __init__(self,board):
        super().__init__(board)
        self.img = pygame.image.load("resource/slow.png")
        self.cost = 75
        self.hp = 100
        self.time = 40
        self.timeuntilaction = 30
        self.dmg = 2
    def action(self):
            enemy_list = self.board.give_enemy()
            target = self.search(enemy_list)
            if target != False:
                self.board.add_projectile(projectile_slow(self.dmg,target,[self.positionx,self.positiony],self.board))
class poisoner(shooter):
    def __init__(self,board):
        super().__init__(board)
        self.img = pygame.image.load("resource/poison.png")
        self.cost = 175
        self.hp = 100
        self.time = 40
        self.timeuntilaction = 40
        self.dmg = 2
    def action(self):
            enemy_list = self.board.give_enemy()
            target = self.search(enemy_list)
            if target != False:
                self.board.add_projectile(projectile_poison(self.dmg,target,[self.positionx,self.positiony],self.board))

class projectile:
    def __init__(self,dmg,target,location,board):
        self.dmg = dmg
        self.target = target
        self.targetxy = target.xypos()
        self.location = location
        self.hp = 1
        self.img = pygame.image.load("resource/projectile.png")
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
        self.img = pygame.image.load("resource/slow_project.png")
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
        self.img = pygame.image.load("resource/poison_proj.png")
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


class Debuff:
    def __init__(self,duration,target):
        self.duration = duration
        self.remaining_duration = duration
        self.target = target
    def tick(self):
        self.remaining_duration -= 1
        self.effect()
        return self.remaining_duration > 0
    def name(self):
        return self.name
    def reset(self):
        self.remaining_duration = self.duration

class PoisonDebuff(Debuff):
    def __init__(self,duration,target):
        self.name = "P"
        super().__init__(duration,target)
    def effect(self):
        self.target.loosehp(0.1)
    def effectgone(self):
        pass

class SlowDebuff(Debuff):
    def __init__(self,duration,target):
        self.name = "S"
        super().__init__(duration,target)
        self.applied = False
    def effect(self):
        if self.applied == False:
            self.applied = True
            self.target.speedmodi(0.5)
    def effectgone(self):
        self.target.speedmodi(2)

def plantings(x,y,plant,price):
    for i in game.plots:
        if i.checkclick(x,y) and i.planted():
            i.planting(plant,price)

def clickeditem(x,y):
    for i in game.give_entity():
        if i.ifclicked(x,y):
            return i
    return False
def mergeSort(nums):
    if len(nums) < 2:
        return nums
    mid = len(nums) // 2
    left = mergeSort(nums[:mid])
    right = mergeSort(nums[mid:])

    i = j = 0
    result = []
    while i < len(left) and j < len(right):
        if left[i] < right[j]: 
            result.append(left[i])
            i += 1
        else: 
            result.append(right[j])
            j += 1

    while i < len(left): 
        result.append(left[i]) 
        i += 1

    while j < len(right): 
        result.append(right[j]) 
        j += 1

    return result

def actions(object):
    object.timeuntilaction -= 0.1
    if object.timeuntilaction <= 0:
        object.action()
        object.timeuntilaction = object.time
enemyspawntime = 500
def spawnsmth(entryspot,enemyspawntime,time):
    if time < 4000:
        if enemyspawntime <=0:
            game.add_enemy(Basic(entryspot,game))
            game.enemy_list[-1].update_direction()
            enemyspawntime = random.randint(500,1000)
        else:
            enemyspawntime -= 1
    else:
        if enemyspawntime <=0:
            a = random.randint(1,3)
            if a == 1:
                temp = Basic(entryspot,game)
            elif a ==2:
                temp = Speed(entryspot,game)
            else:
                temp = Tank(entryspot,game)
            game.add_enemy(temp)
            game.enemy_list[-1].update_direction()
            enemyspawntime = random.randint(500,1000)
        else:
            enemyspawntime -= 2
    return enemyspawntime

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

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
defaultplant = plant("nothing")
game = board(screen,defaultplant)

def main():
    running = True
    dt = 0
    preset= mapgen.preset
    entry = mapgen.start
    print (entry)
    current = copy.copy(entry)
    game.createboard()
    path_image = pygame.image.load("resource/path.png")
    path_image = pygame.transform.scale(path_image, (60,60))

    for i in range(len(preset)):
        game.changegrid(current[0],current[1],int(preset[i]),path_image)
        if preset[i] == "1":
            current[0] += 1
        if preset[i] == "2":
            current[1] -= 1
        if preset[i] == "3":
            current[0] -= 1
        if preset[i] == "4":
            current[1] += 1

    end_image = pygame.image.load("resource/end.png")
    end_image = pygame.transform.scale(end_image, (60,60))

    game.changegrid(current[0],current[1],"end",end_image)
    holdingitem = False
    sunflowerslot= slot(sunflower(game),120,1,game)
    shooterslot = slot(shooter(game),200,1,game)

    game.add_entity(sunflowerslot)
    game.add_entity(shooterslot)
    slowerslot = slot(slower(game),280,1,game)
    game.add_entity(slowerslot)
    poisonslot = slot(poisoner(game),360,1,game)
    game.add_entity(poisonslot)

    enemyspawntime = 500
    font = pygame.font.Font(None, 74)
    white = (255, 255, 255)
    time = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                    
        if game.give_playerhealth() == 0:
            running = False
            print ("FAIL")
        slotimg = pygame.image.load("resource/9_Seed_Slots.webp")
        slot_size = (900,100)
        slotimg = pygame.transform.scale(slotimg,slot_size)
        img = pygame.image.load("resource/download.jpg")
        DEFAULT_IMAGE_SIZE = (1280, 720)
        img = pygame.transform.scale(img, DEFAULT_IMAGE_SIZE)
        screen.blit(img,(0,0))
        screen.blit(slotimg,(0,0))
        game.drawboard()
        for i in game.give_entity():
            i.display()
        
        dt = clock.tick(100)
        #everything below is to update things every tick.
        time += 1

        player_pos = (pygame.mouse.get_pos()) 
        xcord = (player_pos[0]-120)//60
        ycord = (player_pos[1]-100)//60
        if pygame.mouse.get_pressed()[0] and not holdingitem:
            clickcheck = clickeditem(player_pos[0],player_pos[1])
            print("clicked")
            if clickcheck != False:
                holdingitem = True
                print("holding")
        if holdingitem:
            clickcheck.display1(player_pos[0],player_pos[1])
        if pygame.mouse.get_pressed()[2] and holdingitem:
            plantings(xcord,ycord,copy.copy(clickcheck.plant),clickcheck.getprice())
            holdingitem = False
        enemyspawntime = spawnsmth(copy.copy(entry),enemyspawntime,time)
        game.allentity()
        sunlight = game.give_sun()
        display_sunlight = font.render(str(sunlight), True, white)
        sunlight_rect = display_sunlight.get_rect(center=(200, 150))
        screen.blit(display_sunlight,sunlight_rect)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    '''
    Functionality: 
    '''
    main()
