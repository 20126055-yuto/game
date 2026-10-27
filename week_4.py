import pygame
import random

pygame.init()
screen = pygame.display.set_mode((500,500))
pygame.display.set_caption("Move Hero")
hero_x = 250
hero_y = 250
rect_x =100
rect_y =100
my_font = pygame.font.SysFont(None,50)
speed = 20
running = True
snake =[]
for i in range(6):
    snake.append((hero_x))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT:
                speed =170
            hero_color = (255,0,0)
            if event.key == pygame.K_UP:
                hero_y -=speed
                
            if event.key == pygame.K_DOWN:
                hero_y +=speed
                
            if event.key == pygame.K_LEFT:
                hero_x -=speed
                
            if event.key == pygame.K_RIGHT:
                hero_x +=speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT:
                speed =20
            hero_color = (255,0,0)
    screen.fill((209,27,227))
    pygame.draw.circle(screen,(0,200,0),(hero_x,hero_y),20)
    pygame.draw.circle(screen,(255,255,255),(hero_x+6,hero_y-5),4)
    pygame.draw.circle(screen,(255,255,255),(hero_x+6,hero_y+5),4)
    pygame.draw.circle(screen,(0,0,0),(hero_x+6,hero_y-5),2)
    pygame.draw.circle(screen,(0,0,0),(hero_x+6,hero_y+5),2)
    pygame.draw.circle(screen,(0,180,0),(hero_x-18,hero_y),12)
    pygame.draw.circle(screen,(0,160,0),(hero_x-32,hero_y),10)
    pygame.draw.circle(screen,(0,140,0),(hero_x-44,hero_y),8)
    pygame.draw.circle(screen,(0,120,0),(hero_x-54,hero_y),6)
    pygame.draw.circle(screen,(0,100,0),(hero_x-62,hero_y),4)
    pygame.draw.line(screen,(255,0,0),(hero_x+20,hero_y),(hero_x+30,hero_y-4),2)
    pygame.draw.rect(screen,(217,234,19),(rect_x,rect_y,30,30),30)
    if(abs(hero_x - rect_x)<30 and abs(hero_y-rect_y)<30):
        rect_x =random.randint(20,480)
        rect_y =random.randint(20,480)

    if(hero_x>500 or hero_x<0 or hero_y>500 or hero_y <0):
        msg =my_font.render("Game Over", True, (239,244,234))
        screen.blit(msg,(150,200))
    pygame.display.update()
    
pygame.quit()