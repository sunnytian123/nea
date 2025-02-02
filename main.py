#todo readme graphic, python doc,comment class, change enemy.update_direction so it doesnt search everything, python enum
#more enemy class, make maze gen 1d
import pygame
import copy
import random
import src.mapgen
from src.enemy import Basic,Speed,Tank
from src.plant import plant,sunflower,shooter,slower,poisoner
from src.board_classes import board,slot



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



pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
defaultplant = plant("nothing")
game = board(screen,defaultplant)

def main():
    enemyspawntime = 500
    running = True
    dt = 0
    preset= src.mapgen.preset
    entry = src.mapgen.start
    print (entry)
    current = copy.copy(entry)
    game.createboard()
    path_image = pygame.image.load("./resource/path.png")
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

    end_image = pygame.image.load("./resource/end.png")
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
        slotimg = pygame.image.load("./resource/9_Seed_Slots.webp")
        slot_size = (900,100)
        slotimg = pygame.transform.scale(slotimg,slot_size)
        img = pygame.image.load("./resource/download.jpg")
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
            clickcheck = game.clickeditem(player_pos[0],player_pos[1])
            print("clicked")
            if clickcheck != False:
                holdingitem = True
                print("holding")
        if holdingitem:
            clickcheck.display1(player_pos[0],player_pos[1])
        if pygame.mouse.get_pressed()[2] and holdingitem:
            game.plantings(xcord,ycord,copy.copy(clickcheck.plant),clickcheck.getprice())
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
