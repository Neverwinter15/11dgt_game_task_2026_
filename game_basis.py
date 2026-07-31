import pygame
import random
import time

# pygame setup
pygame.init()
screen = pygame.display.set_mode((0, 0),pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, round(screen.get_height() / 2, -2))
target_pos = (1000, 300)
def move(target_pos, mouse_coord):
    target_pos = (round(mouse_coord[0], -2), round(mouse_coord[1], -2))
    return target_pos

def pathfind(player_pos, target_pos):
    up_down = 0
    left_right = 0
    if player_pos[0] == target_pos[0] and player_pos[1] == target_pos[1]:
        direction = 0
        return direction
    if player_pos[0] > target_pos[0]:
        left_right = 1
    elif player_pos[0] < target_pos[0]:
        left_right = 2
    if player_pos[1] < target_pos[1]:
        up_down = 3
    elif player_pos[1] > target_pos[1]:
        up_down = 4
    if up_down != 0 and left_right != 0:
        choose = random.randint(1,2)
        if choose == 1:
            direction = up_down
        else:
            direction = left_right
    elif up_down != 0:
        direction = up_down
    else:
        direction = left_right
    return direction
    
walk = False

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("green")
    

    pygame.draw.circle(screen, "red", player_pos, 40)
    
    
    
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
    if keys[pygame.K_w]:
        mouse_coord = pygame.mouse.get_pos()
        target_pos = move(target_pos, mouse_coord)
        walk = True
    if walk == True:
        direction = pathfind(player_pos, target_pos)
        if direction == 0:
            walk = False
        elif direction == 1:
            player_pos.x -= 100
        elif direction == 2:
            player_pos.x += 100
        elif direction == 3:
            player_pos.y += 100
        elif direction == 4:
            player_pos.y -= 100
        
        mouse_coord = pygame.mouse.get_pos()
        target_pos = move(target_pos, mouse_coord)
        time.sleep(.25)
        

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()