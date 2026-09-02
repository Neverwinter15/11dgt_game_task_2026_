import pygame
import random
import time

# pygame setup
pygame.init()
# makes game full screen
screen = pygame.display.set_mode((1000,800))
clock = pygame.time.Clock()
running = True
font = pygame.font.Font(None, 36)
dt = 0
turn = True
b_m_coords = pygame.Vector2(round(screen.get_width() / 2, -2), round(screen.get_height() / 2, -2))
b_r_coords = pygame.Vector2(round(screen.get_width() / 4, -2), round(screen.get_height() / 4, -2))
b_c_coords = pygame.Vector2(round(screen.get_width() / 7, -2), round(screen.get_height() / 7, -2))
m_m_coords = pygame.Vector2(round(screen.get_width() / 3, -2), round(screen.get_height() / 3, -2))
m_r_coords = pygame.Vector2(round(screen.get_width() / 5, -2), round(screen.get_height() / 3, -2))
m_c_coords = pygame.Vector2(round(screen.get_width() / 2, -2), round(screen.get_height() / 4, -2))
turn_order = "" 

target_pos = (1000, 300)
maori_target_pos = (1000, 300)
#variables to help record if a sprite has been clicked and cords
sprite_clicked = False
maori_sprite_clicked = False
next_coordinates = None
next_maori_coordinates = None

images = {
    "b_melee_1": pygame.transform.scale(pygame.image.load("images/british_melee_idle.png"), (100, 100)),
    "b_melee_2": pygame.transform.scale(pygame.image.load("images/british_melee_attack.png"), (100, 100)),
    "b_ranged_1": pygame.transform.scale(pygame.image.load("images/british_ranged_idle.png"), (100, 100)),
    "b_ranged_2": pygame.transform.scale(pygame.image.load("images/british_ranged_attack.png"), (100, 100)),
    "b_cavalry_1": pygame.transform.scale(pygame.image.load("images/british_cavalry_idle.png"), (150, 150)),
    "b_cavalry_2": pygame.transform.scale(pygame.image.load("images/british_cavalry_attack.png"), (150, 150)),
    "m_melee_1": pygame.transform.scale(pygame.image.load("images/maori_melee_idle.png"), (100, 100)),
    "m_melee_2": pygame.transform.scale(pygame.image.load("images/maori_melee_attack.png"), (100, 100)),
    "m_ranged_1": pygame.transform.scale(pygame.image.load("images/maori_ranged_idle.png"), (100, 100)),
    "m_ranged_2": pygame.transform.scale(pygame.image.load("images/maori_ranged_attack.png"), (100, 100)),
    "m_cavalry_1": pygame.transform.scale(pygame.image.load("images/maori_cavalry_idle.png"), (150, 150)),
    "m_cavalry_2": pygame.transform.scale(pygame.image.load("images/maori_cavalry_attack.png"), (150, 150))
}

def pathfind(unit_pos, target_pos):
    up_down = 0
    left_right = 0
    if unit_pos[0] == target_pos[0] and unit_pos[1] == target_pos[1]:
        direction = 0
        return direction
    if unit_pos[0] > target_pos[0]:
        left_right = 1
    elif unit_pos[0] < target_pos[0]:
        left_right = 2
    if unit_pos[1] < target_pos[1]:
        up_down = 3
    elif unit_pos[1] > target_pos[1]:
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

#compacted movement into a function.

b_m_walk = False
m_m_walk = False


#detects when it is clicked
def on_click():
    global sprite_clicked
    sprite_clicked = True
def on_maori_click():
    global maori_sprite_clicked
    maori_sprite_clicked = True 

x_cords = b_m_coords[0]
y_cords = b_m_coords[1]

#set strength, mana stats, health and steps per turn for all of the melee units
melee_strength = 4
melee_health = 10
melee_mana_cost = 2
melee_steps = 4
melee_range = 150

#set strength, mana stats, health and steps per turn for all of the ranged units
ranged_strength = 6
ranged_health = 8
ranged_mana_cost = 3
ranged_steps = 2
ranged_damage_range = 300

#set strength, mana stats, health and steps per turn for all of the cavalry units
cavalry_strength = 8
cavalry_health = 12
cavalry_mana_cost = 5
cavalry_steps = 7
cavalry_range = 150

#this defines the object for a British melee sprite
class BritishMeleeSprite(pygame.sprite.Sprite):
    def __init__(self, coords, image, callback):
        global b_m_coords
        super().__init__()
        #x = x_cords
        #y = y_cords
        self.image = image
        # self.image.fill((0, 0, 255)) 
        self.rect = self.image.get_rect()
        self.rect.x = round(int(coords[0]), -2)
        self.rect.y = round(int(coords[1]), -2)
        self.callback = callback
        self.health = melee_health
        self.strength = melee_strength
        self.Alive = True
        
    #update code makes the sprite act and updates visual
    def update(self, coords, events, image):
        self.image = image
        self.rect.x = int(coords[0])
        self.rect.y = int(coords[1])
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.callback()
                    return True 
        return False
    def damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.Alive = False
            group.remove(b_m_sprite)
    
    def move(self, target_pos):
        #player_pos and walk were made global for simplicity
        global b_m_walk
        global b_m_coords
        #same walking code as before, it changes player coordinates based on direction from pathfind code
        direction = pathfind(b_m_coords, target_pos)
        if direction == 0:
            b_m_walk = False
        elif direction == 1:
            b_m_coords.x -= 100
        elif direction == 2:
            b_m_coords.x += 100
        elif direction == 3:
            b_m_coords.y += 100
        elif direction == 4:
            b_m_coords.y -= 100


b_m_sprite = BritishMeleeSprite(b_m_coords, images["b_melee_1"], on_click)

#this defines the object for a British ranged sprite
class BritishRangedSprite(pygame.sprite.Sprite):
    def __init__(self, image, callback):
        global b_r_coords
        super().__init__()
        #x = x_cords
        #y = y_cords
        self.image = image
        # self.image.fill((0, 0, 255)) 
        self.rect = self.image.get_rect()
        self.rect.x = round(int(b_r_coords.x), -2)
        self.rect.y = round(int(b_r_coords.y), -2)
        self.callback = callback
        self.health = ranged_health
        self.strength = ranged_strength
        self.Alive = True
        
    #update code makes the sprite act and updates visual
    def update(self, events, image):
        self.image = image
        self.rect.x = int(b_r_coords.x)
        self.rect.y = int(b_r_coords.y)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.callback()
                    return True 
        return False
    def damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.Alive = False
            group.remove(b_r_sprite)
    
    def move(self, target_pos):
        #player_pos and walk were made global for simplicity
        global b_r_walk
        #same walking code as before, it changes player coordinates based on direction from pathfind code
        direction = pathfind(target_pos)
        if direction == 0:
            b_r_walk = False
        elif direction == 1:
            b_r_coords.x -= 100
        elif direction == 2:
            b_r_coords.x += 100
        elif direction == 3:
            b_r_coords.y += 100
        elif direction == 4:
            b_r_coords.y -= 100

b_r_sprite = BritishRangedSprite(images["b_ranged_1"], on_click)

#this defines the object for a British cavalry sprite
class BritishCavalrySprite(pygame.sprite.Sprite):
    def __init__(self, image, callback):
        global b_c_coords
        super().__init__()
        #x = x_cords
        #y = y_cords
        self.image = image
        # self.image.fill((0, 0, 255)) 
        self.rect = self.image.get_rect()
        self.rect.x = round(int(b_c_coords.x), -2)
        self.rect.y = round(int(b_c_coords.y), -2)
        self.callback = callback
        self.health = ranged_health
        self.strength = ranged_strength
        self.Alive = True
        
    #update code makes the sprite act and updates visual
    def update(self, events, image):
        self.image = image
        self.rect.x = int(b_c_coords.x)
        self.rect.y = int(b_c_coords.y)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.callback()
                    return True 
        return False
    def damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.Alive = False
            group.remove(b_c_sprite)
    
    def move(self, target_pos):
        #player_pos and walk were made global for simplicity
        global b_c_walk
        #same walking code as before, it changes player coordinates based on direction from pathfind code
        direction = pathfind(target_pos)
        if direction == 0:
            b_c_walk = False
        elif direction == 1:
            b_c_coords.x -= 100
        elif direction == 2:
            b_c_coords.x += 100
        elif direction == 3:
            b_c_coords.y += 100
        elif direction == 4:
            b_c_coords.y -= 100

b_c_sprite = BritishCavalrySprite(images["b_cavalry_1"], on_click)

#this defines the object for a Maori melee sprite
class MaoriMeleeSprite(pygame.sprite.Sprite):
    def __init__(self, coords, image, callback):
        global m_m_coords
        super().__init__()
        #x = x_cords
        #y = y_cords
        self.image = image
        # self.image.fill((0, 0, 255)) 
        self.rect = self.image.get_rect()
        self.rect.x = round(coords[0], -2)
        self.rect.y = round(coords[1], -2)
        self.callback = callback
        self.health = melee_health
        self.strength = melee_strength
        self.Alive = True
        
    #update code makes the sprite act and updates visual
    def update(self, coords, events, image):
        self.image = image
        self.rect.x = int(coords[0])
        self.rect.y = int(coords[1])
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.callback()
                    return True 
        return False
    def damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.Alive = False
            group.remove(m_m_sprite)
    
    def move(self, target_pos):
        #player_pos and walk were made global for simplicity
        global m_m_walk
        global m_m_coords
        #same walking code as before, it changes player coordinates based on direction from pathfind code
        direction = pathfind(m_m_coords, target_pos)
        if direction == 0:
            m_m_walk = False
        elif direction == 1:
            m_m_coords.x -= 100
        elif direction == 2:
            m_m_coords.x += 100
        elif direction == 3:
            m_m_coords.y += 100
        elif direction == 4:
            m_m_coords.y -= 100


m_m_sprite = MaoriMeleeSprite(m_m_coords, images["m_melee_1"], on_maori_click)

#this defines the object for a Maori ranged sprite
class MaoriRangedSprite(pygame.sprite.Sprite):
    def __init__(self, image, callback):
        global m_r_coords
        super().__init__()
        #x = x_cords
        #y = y_cords
        self.image = image
        # self.image.fill((0, 0, 255)) 
        self.rect = self.image.get_rect()
        self.rect.x = round(int(m_r_coords.x), -2)
        self.rect.y = round(int(m_r_coords.y), -2)
        self.callback = callback
        self.health = ranged_health
        self.strength = ranged_strength
        self.Alive = True
        
    #update code makes the sprite act and updates visual
    def update(self, events, image):
        self.image = image
        self.rect.x = int(m_r_coords.x)
        self.rect.y = int(m_r_coords.y)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.callback()
                    return True 
        return False
    def damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.Alive = False
            group.remove(m_r_sprite)
 
    def move(self, target_pos):
        #player_pos and walk were made global for simplicity
        global m_r_walk
        #same walking code as before, it changes player coordinates based on direction from pathfind code
        direction = pathfind(target_pos)
        if direction == 0:
            m_r_walk = False
        elif direction == 1:
            m_r_coords.x -= 100
        elif direction == 2:
            m_r_coords.x += 100
        elif direction == 3:
            m_r_coords.y += 100
        elif direction == 4:
            m_r_coords.y -= 100


m_r_sprite = MaoriRangedSprite(images["m_ranged_1"], on_maori_click)

#this defines the object for a Maori ranged sprite
class MaoriCavalrySprite(pygame.sprite.Sprite):
    def __init__(self, image, callback):
        global m_c_coords
        super().__init__()
        #x = x_cords
        #y = y_cords
        self.image = image
        # self.image.fill((0, 0, 255)) 
        self.rect = self.image.get_rect()
        self.rect.x = round(int(m_c_coords.x), -2)
        self.rect.y = round(int(m_c_coords.y), -2)
        self.callback = callback
        self.health = cavalry_health
        self.strength = cavalry_strength
        self.Alive = True
        
    #update code makes the sprite act and updates visual
    def update(self, events, image):
        self.image = image
        self.rect.x = int(m_c_coords.x)
        self.rect.y = int(m_c_coords.y)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.callback()
                    return True 
        return False
    def damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.Alive = False
            group.remove(m_c_sprite)
    
    def move(self, target_pos):
        #player_pos and walk were made global for simplicity
        global m_c_walk
        #same walking code as before, it changes player coordinates based on direction from pathfind code
        direction = pathfind(target_pos)
        if direction == 0:
            m_c_walk = False
        elif direction == 1:
            m_c_coords.x -= 100
        elif direction == 2:
            m_c_coords.x += 100
        elif direction == 3:
            m_c_coords.y += 100
        elif direction == 4:
            m_c_coords.y -= 100


m_c_sprite = MaoriCavalrySprite(images["m_cavalry_1"], on_maori_click)

group = pygame.sprite.Group(b_m_sprite, b_r_sprite, b_c_sprite, m_m_sprite, m_r_sprite, m_c_sprite)




while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            

        if event.type == pygame.MOUSEBUTTONDOWN and sprite_clicked:# checks if sprite is clicked and mouse is clicked
            if not b_m_sprite.rect.collidepoint(event.pos): 
                if turn == True:
                 next_coordinates = event.pos
                 next_coordinates = (round(int(next_coordinates[0]), -2), round(int(next_coordinates[1]), -2))
                 sprite_clicked = False
                 b_m_walk = True
                else:
                  b_m_walk == False
       
        if event.type == pygame.MOUSEBUTTONDOWN and maori_sprite_clicked:
            if not m_m_sprite.rect.collidepoint(event.pos):
                if turn == False: 
                 next_maori_coordinates = event.pos
                 next_maori_coordinates = (round(int(next_maori_coordinates[0]), -2), round(int(next_maori_coordinates[1]), -2))
                 maori_sprite_clicked = False
                 m_m_walk = True
                else:
                  m_m_walk = False
          
    #shuts down the game when k button is pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False
    if keys[pygame.K_LEFT]:
        if turn == True:
           turn = False
    if keys[pygame.K_RIGHT]:
        if turn ==False:
          turn=True
  
    target_pos = next_coordinates
    maori_target_pos = next_maori_coordinates

    proximity_distance = m_m_coords.distance_to(b_m_coords)

    range = proximity_distance < 200

    if b_m_walk == True:
        b_m_sprite.move(target_pos)
        time.sleep(0.25)
    if m_m_walk == True:
        m_m_sprite.move(maori_target_pos)
        time.sleep(0.25)

#checks if you are in range to attack. if so, updates sprites in attack pose
    range = proximity_distance > 200
    cooldown = 0
    if range == False and b_m_walk == False and cooldown == 0:
        attack = True
    else:
        attack = False

    if attack == True:
        b_m_sprite.update(b_m_coords, events, images["b_melee_2"])
        m_m_sprite.damage(1)
        attack = False
        cooldown = 2000

    else:
        b_m_sprite.update(b_m_coords, events, images["b_melee_1"])
        m_m_sprite.update(m_m_coords, events, images["m_melee_1"])
        if cooldown > 0:
            cooldown -= 1
    m_m_sprite.update(m_m_coords, events, images["m_melee_1"])
    


    # fill the screen with a color to wipe away anything from last frame
    screen.fill("green")


    group.draw(screen)# displays sprite


    # checks if sprite was clicked
    #if sprite_clicked:
      #  status_str = "sprite clicked"
    
    #elif next_maori_coordinates:
     #   status_str = f"recorded: {next_maori_coordinates}"#displays cords of second click
       # m_m_walk = True
   # elif next_coordinates:
   #     status_str = f"recorded: {next_coordinates}"#displays cords of second click
   #     b_m_walk = True
   # else:# tells you to click
  #      status_str = "click to start."
    
    #status_text = font.render(status_str, True, (0, 0, 0))
    #screen.blit(status_text, (20, 60))
    
    if turn == True:
        turn_order = "British turn"

    elif turn == False:
        turn_order = "Māori turn"
    
    if turn == True:
        make_turn = "press right arrow to end turn"
    else: 
        make_turn = "press left arrow to end turn"


    status_text = font.render(turn_order, True, (0, 0, 0))
    screen.blit(status_text, (20, 60))

    turn_instructions = font.render(make_turn, True, (0, 0, 0))
    screen.blit(turn_instructions, (20, 85))


    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(60)# limits FPS to 60
# quits game
pygame.quit()
