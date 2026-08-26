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
b_m_coords = pygame.Vector2(round(screen.get_width() / 2, -2), round(screen.get_height() / 2, -2))
b_r_coords = pygame.Vector2(round(screen.get_width() / 4, -2), round(screen.get_height() / 4, -2))
b_c_coords = pygame.Vector2(round(screen.get_width() / 7, -2), round(screen.get_height() / 7, -2))
m_m_coords = pygame.Vector2(round(screen.get_width() / 3, -2), round(screen.get_height() / 3, -2))
m_r_coords = pygame.Vector2(round(screen.get_width() / 5, -2), round(screen.get_height() / 3, -2))
m_c_coords = pygame.Vector2(round(screen.get_width() / 2, -2), round(screen.get_height() / 4, -2))

target_pos = (1000, 300)
#variables to help record if a sprite has been clicked and cords
sprite_clicked = False
next_coordinates = None

images = {
    "b_melee_1": pygame.transform.scale(pygame.image.load("british_melee_idle.png"), (100, 100)),
    "b_melee_2": pygame.transform.scale(pygame.image.load("british_melee_attack.png"), (100, 100)),
    "b_ranged_1": pygame.transform.scale(pygame.image.load("british_ranged_idle.png"), (100, 100)),
    "b_ranged_2": pygame.transform.scale(pygame.image.load("british_ranged_attack.png"), (100, 100)),
    "b_cavalry_1": pygame.transform.scale(pygame.image.load("british_cavalry_idle.png"), (150, 150)),
    "b_cavalry_2": pygame.transform.scale(pygame.image.load("british_cavalry_attack.png"), (150, 150)),
    "m_melee_1": pygame.transform.scale(pygame.image.load("maori_melee_idle.png"), (100, 100)),
    "m_melee_2": pygame.transform.scale(pygame.image.load("maori_melee_attack.png"), (100, 100)),
    "m_ranged_1": pygame.transform.scale(pygame.image.load("maori_ranged_idle.png"), (100, 100)),
    "m_ranged_2": pygame.transform.scale(pygame.image.load("maori_ranged_attack.png"), (100, 100)),
    "m_cavalry_1": pygame.transform.scale(pygame.image.load("maori_cavalry_idle.png"), (150, 150)),
    "m_cavalry_2": pygame.transform.scale(pygame.image.load("maori_cavalry_attack.png"), (150, 150))
}

def pathfind(target_pos):
    up_down = 0
    left_right = 0
    if b_m_coords[0] == target_pos[0] and b_m_coords[1] == target_pos[1]:
        direction = 0
        return direction
    if b_m_coords[0] > target_pos[0]:
        left_right = 1
    elif b_m_coords[0] < target_pos[0]:
        left_right = 2
    if b_m_coords[1] < target_pos[1]:
        up_down = 3
    elif b_m_coords[1] > target_pos[1]:
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
def move(target_pos):
    #b_m_coords and walk were made global for simplicity
    global walk
#same walking code as before, it changes player coordinates based on direction from pathfind code
    direction = pathfind(target_pos)
    prev_coords = b_m_coords
    if direction == 0:
        walk = False
    elif direction == 1:
        b_m_coords.x -= 100
    elif direction == 2:
        b_m_coords.x += 100
    elif direction == 3:
        b_m_coords.y += 100
    elif direction == 4:
        b_m_coords.y -= 100

walk = False

#detects when it is clicked
def on_click():
    global sprite_clicked
    sprite_clicked = True 


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
    def __init__(self, image, callback):
        global b_m_coords
        super().__init__()
        #x = x_cords
        #y = y_cords
        self.image = image
        # self.image.fill((0, 0, 255)) 
        self.rect = self.image.get_rect()
        self.rect.x = round(int(b_m_coords.x), -2)
        self.rect.y = round(int(b_m_coords.y), -2)
        self.callback = callback
        self.health = melee_health
        self.strength = melee_strength
        self.Alive = True
        
    #update code makes the sprite act and updates visual
    def update(self, events, image):
        self.image = image
        self.rect.x = int(b_m_coords.x)
        self.rect.y = int(b_m_coords.y)
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


b_m_sprite = BritishMeleeSprite(images["b_melee_1"], on_click)

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

b_c_sprite = BritishCavalrySprite(images["b_cavalry_1"], on_click)

#this defines the object for a Maori melee sprite
class MaoriMeleeSprite(pygame.sprite.Sprite):
    def __init__(self, image, callback):
        global m_m_coords
        super().__init__()
        #x = x_cords
        #y = y_cords
        self.image = image
        # self.image.fill((0, 0, 255)) 
        self.rect = self.image.get_rect()
        self.rect.x = round(int(m_m_coords.x), -2)
        self.rect.y = round(int(m_m_coords.y), -2)
        self.callback = callback
        self.health = melee_health
        self.strength = melee_strength
        self.Alive = True
        
    #update code makes the sprite act and updates visual
    def update(self, events, image):
        self.image = image
        self.rect.x = int(m_m_coords.x)
        self.rect.y = int(m_m_coords.y)
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


m_m_sprite = MaoriMeleeSprite(images["m_melee_1"], on_click)

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


m_r_sprite = MaoriRangedSprite(images["m_ranged_1"], on_click)

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


m_c_sprite = MaoriCavalrySprite(images["m_cavalry_1"], on_click)

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
                next_coordinates = event.pos
                next_coordinates = (round(int(next_coordinates[0]), -2), round(int(next_coordinates[1]), -2))
                sprite_clicked = False
                walk = True

    #shuts down the game when esc button is pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False
  
    target_pos = next_coordinates

    proximity_distance = m_m_coords.distance_to(b_m_coords)
    proximity_distance2 = m_r_coords.distance_to(b_m_coords)
    proximity_distance3 = m_c_coords.distance_to(b_m_coords)

    range = proximity_distance > 200

    if walk == True:
            move(target_pos)
            time.sleep(0.25)

    #checks if you are in range to attack melee Maori unit. if so, updates sprites in attack pose
    range = proximity_distance > melee_range
    if range == False and walk == False:
        attack = True
    else:
        attack = False

    if attack == True:
        b_m_sprite.update(events, images["b_melee_2"])
        m_m_sprite.damage(melee_strength)
    else:
        b_m_sprite.update(events, images["b_melee_1"])

    #checks if you are in range to attack ranged Maori unit. if so, updates sprites in attack pose
    range = proximity_distance2 > melee_range
    if range == False and walk == False:
        attack = True
    else:
        attack = False

    if attack == True:
        b_m_sprite.update(events, images["b_melee_2"])
        m_r_sprite.damage(melee_strength)
    else:
        b_m_sprite.update(events, images["b_melee_1"])

    #checks if you are in range to attack cavalry Maori unit. if so, updates sprites in attack pose
    range = proximity_distance3 > melee_range
    if range == False and walk == False:
        attack = True
    else:
        attack = False

    if attack == True:
        b_m_sprite.update(events, images["b_melee_2"])
        m_c_sprite.damage(melee_strength)
    else:
        b_m_sprite.update(events, images["b_melee_1"])

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("green")


    group.draw(screen)# displays sprite


   # gets cords of the mouse
   # credits to Pygame Get Mouse Position
   #https://medium.com/@amit25173/pygame-get-mouse-position-6096677f49e3
   # the code from this website just displays the cords of the mouse and saves it as a  variable
   
    # checks if sprite was clicked
    if sprite_clicked:
        status_str = "sprite clicked"
    elif next_coordinates:
        status_str = f"recorded: {next_coordinates}"#displays cords of second click
        walk = True
    else:# tells you to click
        status_str = "click to start."
    
    status_text = font.render(status_str, True, (0, 0, 0))
    screen.blit(status_text, (20, 60))
    
    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(60)# limits FPS to 60
# quits game
pygame.quit()