import pygame
import math
from .board_classes import projectile, projectile_poison,projectile_slow
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
        self.img = pygame.image.load("./resource/sunflower.png")
        self.cost = 100
        self.hp = 100
        self.time = 50
        self.timeuntilaction = 50
    def action(self):
        self.board.update_sun(100)
class shooter(plant):
    def __init__(self,board):
        super().__init__(board)
        self.img = pygame.image.load("./resource/bow.png")
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
        self.img = pygame.image.load("./resource/slow.png")
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
        self.img = pygame.image.load("./resource/poison.png")
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
