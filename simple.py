import pygame
pygame.init()

screen = pygame.display.set_mode((500,500))
pygame.display.set_caption("Auto Move")
ball_x = 250
ball_y = 250
speed = 5
running = True

direction_x = 0
direction_y = 0
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                direction_x=0
                direction_y=-5
            elif event.key == pygame.K_DOWN:
                direction_x=0
                direction_y=5
            elif event.key == pygame.K_LEFT:
                direction_x=-5
                direction_y=0
            elif event.key == pygame.K_RIGHT:
                direction_x=5
                direction_y=0
    ball_x += direction_x
    ball_y += direction_y
    screen.fill((30,30,30))
    pygame.draw.circle(screen,(255,0,0),(ball_x,ball_y),10)
    pygame.display.update()
    clock.tick(60)
pygame.quit()