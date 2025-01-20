import pygame
class enemy:
    def __init__(self,start,board):
        self.hp = 0
        self.speed = 0
        self.img = 0
        self.current_direction = 0
        self.pos = start
        self.distance_till_next = 0
        self.board = board
        self.debuff = []
    def add_debuff(self,debuff):
        for i in self.debuff:
            if i.name == debuff.name:
                i.reset()
                return i
        self.debuff.append(debuff)
    def update_debuff(self):
        for i in self.debuff:
            if not i.tick():
                i.effectgone()
                self.debuff.remove(i)
    def check_direction(self):
        for i in self.board.give_plots():
            if i.givexy() == self.pos:
                self.current_direction = i.givetype()
                if i.givetype() == "end":
                    self.board.loosehp()
                    print ("lost hp")
                    self.hp = 0
    def action(self):
        if self.distance_till_next>0:
            self.move()
        else:
            if self.current_direction == 4:
                self.pos[1] += 1
            if self.current_direction == 3:
                self.pos[0] = self.pos[0] - 1
            if self.current_direction == 2:
                self.pos[1] = self.pos[1] -1
            if self.current_direction == 1:
                self.pos[0] += 1
            self.check_direction()
            self.distance_till_next = 60
        self.display()
    def move(self):
        self.update_debuff()
        self.distance_till_next = self.distance_till_next-self.speed
    def xypos(self):
        x = self.pos[0]*60+130
        y = self.pos[1]*60+110
        distance_moved = 60-self.distance_till_next
        if self.current_direction == 4:
            y += distance_moved
        if self.current_direction == 3:
            x = x - distance_moved
        if self.current_direction == 2:
            y = y -distance_moved
        if self.current_direction == 1:
            x += distance_moved
        return [x,y]
    def display(self):
        xycord = self.xypos()
        enemyimg =self.img
        DEFAULT_IMAGE_SIZE = (40, 40)
        enemyimg = pygame.transform.scale(enemyimg, DEFAULT_IMAGE_SIZE)
        self.board.give_screen().blit(enemyimg,xycord)
    def loosehp(self,dmg):
        self.hp = self.hp-dmg
    def speedmodi(self,modi):
        self.speed = self.speed*modi

        

class basic(enemy):
    def __init__(self,start,board):
        super().__init__(start,board)
        self.hp = 100
        self.speed = 1
        self.img = pygame.image.load("resource/henrymak.jpg")
class tank(enemy):
    def __init__(self,start,board):
        super().__init__(start,board)
        self.hp = 400
        self.speed = 0.5
        self.img = pygame.image.load("resource/tank.png")
class speed(enemy):
    def __init__(self,start,board):
        super().__init__(start,board)
        self.hp = 60
        self.speed = 2
        self.img = pygame.image.load("resource/speed.png")


