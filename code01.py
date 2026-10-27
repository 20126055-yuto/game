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
direction_x = speed
direction_y = 0
score = 0
clock = pygame.time.Clock()

snake = []
for i in range(6):
    snake.append((hero_x-i*30, hero_y))
pygame.mixer.init()
sound = pygame.mixer.Sound("voice.mp3")
running = True
game_over = False
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                direction_x= 0
                direction_y = -speed
            elif event.key == pygame.K_DOWN:
                direction_x= 0
                direction_y = speed
            elif event.key == pygame.K_LEFT:
                direction_x= -speed
                direction_y = 0
            elif event.key == pygame.K_RIGHT:
                direction_x= speed
                direction_y = 0
            elif event.key == pygame.K_LSHIFT:
                speed = 40
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT:
                speed =20
                if direction_x >0:
                    direction_x =speed
                elif direction_x <0:
                    direction_x =-speed
                elif direction_y >0:
                    direction_y =speed
                elif direction_y<0:
                    direction_y= -speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT:
                speed =20
                if direction_x >0:
                    direction_x =speed
                elif direction_x <0:
                    direction_x =-speed
                elif direction_y >0:
                    direction_y =speed
                elif direction_y<0:
                    direction_y= -speed
               
    

    hero_x +=direction_x
    hero_y +=direction_y
    snake.insert(0,(hero_x,hero_y))
    snake.pop()

    screen.fill((75,77,73))
    score_surface = my_font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_surface, (10, 10)) # 左上に表示
    for i ,(x,y) in enumerate(snake):
        if i ==0:
            pygame.draw.circle(screen,(0,200,0),(x,y),20)
            pygame.draw.circle(screen,(255,255,255),(x+6,y-5),4)
            pygame.draw.circle(screen,(255,255,255),(x+6,y+5),4)

            pygame.draw.circle(screen,(0,0,0),(x+6,y-5),2)
            pygame.draw.circle(screen,(0,0,0),(x+6,y+5),2)
            
            pygame.draw.line(screen,(255,0,0),(x+20,y),(x+30,y-4),2)
        else:
            radius = max(4,20 - i * 2)
            green = max(80,200 - i * 20)    
            pygame.draw.circle(screen,(0,green,0),(x,y),radius)
    pygame.draw.rect(screen,(217,234,19),(rect_x,rect_y,30,30),30)
    if(abs(hero_x - rect_x)<30 and abs(hero_y-rect_y)<30):
        rect_x =random.randint(20,480)
        rect_y =random.randint(20,480)
        speed = speed +1
        score += 1
        sound.play()

    if(hero_x>500 or hero_x<0 or hero_y>500 or hero_y <0):
        msg =my_font.render("Game Over", True, (239,244,234))
        screen.blit(msg,(150,200))
        pygame.display.update()
        pygame.time.delay(2000) # 2秒間結果を表示
        running = False

    pygame.display.update()
    clock.tick(10)

pygame.quit()
