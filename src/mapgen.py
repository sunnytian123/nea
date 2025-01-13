import random
class grid():
    def __init__(self,h,l):
        self.boxes = []
        self.h=h
        self.l=l
        self.current = []
        self.start = []
        self.col = []
        self.row = []
    def createboard(self):
        for i in range(self.h):
            for j in range(self.l):
                self.boxes.append(box(j,i,self))
        for i in self.boxes:
            i.get_neighbour()
    def give_box(self,num):
        return self.boxes[num]
    def give_len(self):
        return self.l
    def give_h(self):
        return self.h
    def genmap(self):
        temp = ""
        for i in range(self.l+1):
            temp = ""
            for j in range(self.h):
                temp = temp +"1"
            self.col.append(temp)
        for i in range(self.h+1):
            temp = ""
            for j in range(self.l):
                temp = temp +"1"
            self.row.append(temp)
    def removewall(self,ba,bb):
        b1 = ba.givexy()
        b2 = bb.givexy()
        if b1[0] == b2[0]:
            if b1[1]>b2[1]:
                a = b1[1]
            else:
                a = b2[1]
            b = b1[0]
            temp = list(self.row[a])
            temp[b] = '0'
            newline = ''
            for i in temp:
                newline = newline+i
            self.row[a] = newline
        if b1[1] == b2[1]:
            if b1[0]>b2[0]:
                a = b2[0]+1
            else:
                a = b1[0]+1
            b = b1[1]
            temp = list(self.col[a])
            temp[b] = '0'
            newline =''
            for i in temp:
                newline = newline+i
            self.col[a] = newline

    def boxnum(self,x,y):
        return x+y*self.l
    def makemaze(self):
        self.start = [0,random.randint(0,self.h-1)]
        self.current = self.start
        self.choosenext(self.boxes[self.boxnum(self.start[0],self.start[1])])
    def choosenext(self,box):
        box.visit()
        while box.neighbourlen() >0:
            num = random.randint(0,len(box.neighbour)-1)
            if not box.neighbour[num].if_visited():
                self.removewall(box,box.neighbour[num])
                self.choosenext(box.neighbour[num])
            box.neighbour.pop(num)
class box():
    def __init__(self,x,y,grid):
        self.x = x
        self.y = y
        self.grid = grid
        self.visited = False
        self.neighbour = []
    def givexy(self):
        return [self.x,self.y]
    def visit(self):
        self.visited = True
    def neighbourlen(self):
        return len(self.neighbour)
    def if_visited(self):
        return self.visited
    def give_neighbour(self):
        return self.neighbour
    def get_neighbour(self):
        pos = self.x+self.y*self.grid.give_len()
        if self.x>0:
            temp1 = pos-1
            self.neighbour.append(self.grid.give_box(temp1))
        if self.x+1<self.grid.give_len():
            temp1 = pos+1
            self.neighbour.append(self.grid.give_box(temp1))
        if self.y>0:
            temp1 = pos-self.grid.give_len()
            self.neighbour.append(self.grid.give_box(temp1))
        if self.y+1<self.grid.give_h():
            temp1 = pos+self.grid.give_len()
            self.neighbour.append(self.grid.give_box(temp1))
    
test= grid(9,15)
test.createboard()
test.genmap()
test.makemaze()
maprow = (test.row)
mapcol = (test.col)
class boxs():
    def __init__(self,x,y,num):
        self.num = num
        self.x = x
        self.y = y
        self.neighbour = []
        self.entryorend = False
        self.visited = False
    def neighbours(self,maprow,mapcol):
        if maprow[self.y][self.x] == "0":
            if self.y >0:
                self.neighbour.append(grid[(self.y-1)*(len(mapcol)-1)+self.x])
        if maprow[(self.y)+1][self.x] == "0":
            if self.y+1 < (len(maprow)-1):
                self.neighbour.append(grid[(self.y+1)*(len(mapcol)-1)+self.x])
        if mapcol[self.x][self.y] == "0":
            if self.x >0:
                self.neighbour.append(grid[(self.y)*(len(mapcol)-1)+self.x-1])
        if mapcol[(self.x)+1][self.y] == "0":
            if self.x+1 <(len(mapcol)-1):
                self.neighbour.append(grid[(self.y)*(len(mapcol)-1)+self.x+1])
    def givenum(self):
        return self.num
    def nextto(self):
        return self.neighbour
    def visit(self):
        self.visited = True
    def if_visited(self):
        return self.visited
    def give_x(self):
        return self.x
    def give_y(self):
        return self.y
        
grid = []
current = 1
for i in range(len(maprow)-1):
    for j in range(len(mapcol)-1):
        grid.append(boxs(j,i,current))
        current += 1
for i in grid:
    i.neighbours(maprow,mapcol)
for i in grid:
    i.nextto()
start = [0,random.randint(0,len(maprow)-2)]
end = [len(mapcol)-2,random.randint(0,len(maprow)-2)]
path = []
def pathfind(current):
    current.visit()
    path.append(current)
    if current.give_x()== end[0] and current.give_y() == end[1]:
        return True
    for i in current.nextto():
        if not i.if_visited():
            if pathfind(i):
                return True
    path.pop()
preset =""
pathfind(grid[(start[1])*(len(mapcol)-1)])
for i in range(len(path)):
    if i+1 < len(path):
        temp = path[i+1].givenum() - path[i].givenum()
        if temp == 1:
            preset = preset + "1"
        elif temp == -1:
            preset = preset + "3"
        elif temp == 15:
            preset = preset + "4"
        elif temp == -15:
            preset = preset + "2"
print (preset)
