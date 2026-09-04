import pygame
import random
import time

# pygame setup
pygame.init()
# makes game full screen
screen = pygame.display.set_mode((1000,800))

# Set game name to Tales Of Taranaki
pygame.display.set_caption("Tales Of Taranaki")
#game clock sets tick rate
clock = pygame.time.Clock()
running = True
font = pygame.font.Font(None, 36)
sub_font = pygame.font.Font(None, 50)
sub_sub_font = pygame.font.Font(None, 10)
title_font = pygame.font.Font(None ,100)
dt = 0
turn_choose = random.randint(1,2)
if turn_choose == 1:
    turn = False
if turn_choose == 2:
    turn = True
 #starting coordinates
b_m_coords = pygame.Vector2(200, 400)
b_r_coords = pygame.Vector2(200, 600)
b_c_coords = pygame.Vector2(200, 200)
m_m_coords = pygame.Vector2(800, 600)
m_r_coords = pygame.Vector2(800, 400)
m_c_coords = pygame.Vector2(800, 200)
turn_order = "" 
go = False

bm_target = (1000, 300)
mm_target = (1000, 300)
mr_target = (1000, 300)

# variables to help record if a sprite has been clicked and cords
b_m_clicked = False
b_r_clicked = False
b_c_clicked = False
m_m_clicked = False
m_r_clicked = False
m_c_clicked = False
b_m_next_coords = None
b_r_next_coords = None
b_c_next_coords = None
m_m_next_coords = None
m_r_next_coords = None
m_c_next_coords = None


# Downsize melee and ranged images to 100, 100 and cavalry to 150, 150
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
    "m_cavalry_2": pygame.transform.scale(pygame.image.load("images/maori_cavalry_attack.png"), (150, 150)),
    "gate_pa_bg": pygame.transform.scale(pygame.image.load("images/gate_pa_background.png"), (1000, 800))
}

#decides which way to go
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

#starts as no one walking
b_m_walk = False
b_r_walk = False
b_c_walk = False
m_m_walk = False
m_r_walk = False
m_c_walk = False

#detects when a sprite is clicked
def on_bm_click():
    global b_m_clicked
    b_m_clicked = True
def on_br_click():
    global b_r_clicked
    b_r_clicked = True
def on_bc_click():
    global b_c_clicked
    b_c_clicked = True
def on_mm_click():
    global m_m_clicked
    m_m_clicked = True 
def on_mr_click():
    global m_r_clicked
    m_r_clicked = True
def on_mc_click():
    global m_c_clicked
    m_c_clicked = True


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
        global b_m_coords
        self.health -= damage
        if self.health <= 0:
            b_m_coords = pygame.Vector2(10000,10000)
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


b_m_sprite = BritishMeleeSprite(b_m_coords, images["b_melee_2"], on_bm_click)

#this defines the object for a British ranged sprite
class BritishRangedSprite(pygame.sprite.Sprite):
    def __init__(self, coords, image, callback):
        global b_r_coords
        super().__init__()
        #x = x_cords
        #y = y_cords
        self.image = image
        # self.image.fill((0, 0, 255)) 
        self.rect = self.image.get_rect()
        self.rect.x = round(int(coords[0]), -2)
        self.rect.y = round(int(coords[1]), -2)
        self.callback = callback
        self.health = ranged_health
        self.strength = ranged_strength
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
        global b_r_coords
        self.health -= damage
        if self.health <= 0:
            b_r_coords = pygame.Vector2(10000,10000)
            self.Alive = False
            group.remove(b_r_sprite)
    
    def move(self, target_pos):
        #player_pos and walk were made global for simplicity
        global b_r_walk
        global b_r_coords
        #same walking code as before, it changes player coordinates based on direction from pathfind code
        direction = pathfind(b_r_coords, target_pos)
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

b_r_sprite = BritishRangedSprite(b_r_coords, images["b_ranged_2"], on_br_click)

#this defines the object for a British cavalry sprite
class BritishCavalrySprite(pygame.sprite.Sprite):
    def __init__(self, coords, image, callback):
        global b_c_coords
        super().__init__()
        #x = x_cords
        #y = y_cords
        self.image = image
        # self.image.fill((0, 0, 255)) 
        self.rect = self.image.get_rect()
        self.rect.x = round(int(coords[0]), -2)
        self.rect.y = round(int(coords[1]), -2)
        self.callback = callback
        self.health = ranged_health
        self.strength = ranged_strength
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
        global b_c_coords
        self.health -= damage
        if self.health <= 0:
            b_c_coords = pygame.Vector2(10000,10000)
            self.Alive = False
            group.remove(b_c_sprite)
    
    def move(self, target_pos):
        #player_pos and walk were made global for simplicity
        global b_c_walk
        global b_c_coords
        #same walking code as before, it changes player coordinates based on direction from pathfind code
        direction = pathfind(b_c_coords, target_pos)
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

b_c_sprite = BritishCavalrySprite(b_c_coords, images["b_cavalry_2"], on_bc_click)

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
        global m_m_coords
        self.health -= damage
        if self.health <= 0:
            m_m_coords = pygame.Vector2(10000,10000)
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


m_m_sprite = MaoriMeleeSprite(m_m_coords, images["m_melee_2"], on_mm_click)

#this defines the object for a Maori ranged sprite
class MaoriRangedSprite(pygame.sprite.Sprite):
    def __init__(self, coords, image, callback):
        global m_r_coords
        super().__init__()
        #x = x_cords
        #y = y_cords
        self.image = image
        # self.image.fill((0, 0, 255)) 
        self.rect = self.image.get_rect()
        self.rect.x = round(int(coords[0]), -2)
        self.rect.y = round(int(coords[1]), -2)
        self.callback = callback
        self.health = ranged_health
        self.strength = ranged_strength
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
        #this makes the sprite take damage
    def damage(self, damage):
        global m_r_coords
        self.health -= damage
        if self.health <= 0:
            m_r_coords = pygame.Vector2(10000, 10000)
            self.Alive = False
            group.remove(m_r_sprite)
 #this moves the sprite 
    def move(self, target_pos):
        #player_pos and walk were made global for simplicity
        global m_r_walk
        global m_r_coords
        #same walking code as before, it changes player coordinates based on direction from pathfind code
        direction = pathfind(m_r_coords, target_pos)
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


m_r_sprite = MaoriRangedSprite(m_r_coords, images["m_ranged_2"], on_mr_click)

#this defines the object for a Maori cavalry sprite
class MaoriCavalrySprite(pygame.sprite.Sprite):
    def __init__(self, coords, image, callback):
        global m_c_coords
        super().__init__()
        #x = x_cords
        #y = y_cords
        self.image = image
        # self.image.fill((0, 0, 255)) 
        self.rect = self.image.get_rect()
        self.rect.x = round(int(coords[0]), -2)
        self.rect.y = round(int(coords[1]), -2)
        self.callback = callback
        self.health = cavalry_health
        self.strength = cavalry_strength
        self.Alive = True
        
    #update code makes the sprite act and updates visual. all sprites have this
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
        global m_c_coords
        self.health -= damage
        if self.health <= 0:
            m_c_coords = pygame.Vector2(10000,10000)
            self.Alive = False
            group.remove(m_c_sprite)
    
    def move(self, target_pos):
        #player_pos and walk were made global for simplicity
        global m_c_walk
        global m_c_coords
        #same walking code as before, it changes player coordinates based on direction from pathfind code
        direction = pathfind(m_c_coords, target_pos)
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


m_c_sprite = MaoriCavalrySprite(m_c_coords, images["m_cavalry_2"], on_mc_click)

group = pygame.sprite.Group(b_m_sprite, b_r_sprite, b_c_sprite, m_m_sprite, m_r_sprite, m_c_sprite)


bm_cooldown = 0
mm_cooldown = 0
br_cooldown = 0
mr_cooldown = 0
bc_cooldown = 0
mc_cooldown = 0

#starts the loop
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            
#checks if sprites have been clicked, runs for every sprite
        if event.type == pygame.MOUSEBUTTONDOWN and b_m_clicked:# checks if sprite is clicked and mouse is clicked
            if not b_m_sprite.rect.collidepoint(event.pos): 
                if turn == True:
                 b_m_next_coords = event.pos
                 b_m_next_coords = (round(int(b_m_next_coords[0]), -2), round(int(b_m_next_coords[1]), -2))
                 b_m_clicked = False
                 b_m_walk = True
                else:
                  b_m_walk == False
       
        elif event.type == pygame.MOUSEBUTTONDOWN and m_m_clicked:
            if not m_m_sprite.rect.collidepoint(event.pos):
                if turn == False: 
                    m_m_next_coords = event.pos
                    m_m_next_coords = (round(int(m_m_next_coords[0]), -2), round(int(m_m_next_coords[1]), -2))
                    m_m_clicked = False
                    m_m_walk = True
                else:
                    m_m_walk = False
        elif event.type == pygame.MOUSEBUTTONDOWN and b_r_clicked:
            if not b_r_sprite.rect.collidepoint(event.pos):
                if turn == True:
                    b_r_next_coords = event.pos
                    b_r_next_coords = (round(int(b_r_next_coords[0]), -2), round(int(b_r_next_coords[1]), -2))
                    b_r_clicked = False
                    b_r_walk = True
        elif event.type == pygame.MOUSEBUTTONDOWN and m_r_clicked:
            if not m_r_sprite.rect.collidepoint(event.pos):
                if turn == False:
                    m_r_next_coords = event.pos
                    m_r_next_coords = (round(int(m_r_next_coords[0]), -2), round(int(m_r_next_coords[1]), -2))
                    m_r_clicked = False
                    m_r_walk = True
        elif event.type == pygame.MOUSEBUTTONDOWN and b_c_clicked:
            if not b_c_sprite.rect.collidepoint(event.pos):
                if turn == True:
                    b_c_next_coords = event.pos
                    b_c_next_coords = (round(int(b_c_next_coords[0]), -2), round(int(b_c_next_coords[1]), -2))
                    b_c_clicked = False
                    b_c_walk = True
        elif event.type == pygame.MOUSEBUTTONDOWN and m_c_clicked:
            if not m_c_sprite.rect.collidepoint(event.pos):
                if turn == False:
                    m_c_next_coords = event.pos
                    m_c_next_coords = (round(int(m_c_next_coords[0]), -2), round(int(m_c_next_coords[1]), -2))
                    m_c_clicked = False
                    m_c_walk = True

    #shuts down the game when esc button is pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False
        #starts game and swaps team
    if keys[pygame.K_SPACE]:
        go = True
        if turn == True:
           turn = False
           mm_cooldown = 0
           m_m_walk = False
           mr_cooldown = 0
           m_r_walk = False
           mc_cooldown = 0
           m_c_walk = False
        else:
          turn=True
          bm_cooldown = 0
          b_m_walk = False
          br_cooldown = 0
          b_r_walk = False
          bc_cooldown = 0
          b_c_walk = False
        time.sleep(0.25)

    #sets target
    bm_target = b_m_next_coords
    mm_target = m_m_next_coords
    br_target = b_r_next_coords
    mr_target = m_r_next_coords
    bc_target = b_c_next_coords
    mc_target = m_c_next_coords
#checks proximity
    bm_to_mm = m_m_coords.distance_to(b_m_coords)
    br_to_mm = m_m_coords.distance_to(b_r_coords)
    bm_to_mr = m_r_coords.distance_to(b_m_coords)
    br_to_mr = m_r_coords.distance_to(b_r_coords)
    bc_to_mm = m_m_coords.distance_to(b_c_coords)
    bc_to_mr = m_r_coords.distance_to(b_c_coords)
    bc_to_mc = m_c_coords.distance_to(b_c_coords)
    bm_to_mc = m_c_coords.distance_to(b_m_coords)
    br_to_mc = m_c_coords.distance_to(b_r_coords)
    

#walks around or something
    if b_m_walk == True and bm_cooldown != 1:
        b_m_sprite.move(bm_target)
        time.sleep(0.25)
    if m_m_walk == True and mm_cooldown != 1:
        m_m_sprite.move(mm_target)
        time.sleep(0.25)
    if b_r_walk == True and br_cooldown != 1:
        b_r_sprite.move(br_target)
        time.sleep(0.25)
    if m_r_walk == True and mr_cooldown != 1:
        m_r_sprite.move(mr_target)
        time.sleep(0.25)
    if b_c_walk == True and bc_cooldown != 1:
        b_c_sprite.move(bc_target)
        time.sleep(0.1)
    if m_c_walk == True and mc_cooldown != 1:
        m_c_sprite.move(mc_target)
        time.sleep(0.1)

#checks if you are in range to attack. if so, updates sprites in attack pose
    bm_mm_range = bm_to_mm > melee_range
    br_mm_range = br_to_mm > ranged_damage_range
    mm_br_range = br_to_mm > melee_range
    br_mr_range = br_to_mr > ranged_damage_range
    bm_mr_range = bm_to_mr > melee_range
    mr_bm_range = bm_to_mr > ranged_damage_range
    bc_mc_range = bc_to_mc > cavalry_range
    bc_mm_range = bc_to_mm > cavalry_range
    bc_mr_range = bc_to_mr > cavalry_range
    mr_bc_range = bc_to_mr > ranged_damage_range
    mc_bm_range = bm_to_mc > cavalry_range
    mc_br_range = br_to_mc > cavalry_range
    br_mc_range = br_to_mc > ranged_damage_range



#checks if units can attack
    if bm_mm_range == False and b_m_walk == False and m_m_walk == False and bm_cooldown == 0 and turn == True:
        bm_attack_mm = True
    else:
        bm_attack_mm = False
    if br_mm_range == False and b_r_walk == False and m_m_walk == False and br_cooldown == 0 and turn == True:
        br_attack_mm = True
    else:
        br_attack_mm = False
    if bm_mm_range == False and b_m_walk == False and m_m_walk == False and mm_cooldown == 0 and turn == False:
        mm_attack_bm = True
    else:
        mm_attack_bm = False
    if mm_br_range == False and b_r_walk == False and m_m_walk == False and mm_cooldown == 0 and turn == False:
        mm_attack_br = True
    else:
        mm_attack_br = False
    if mm_br_range == False and b_r_walk == False and m_m_walk == False and mm_cooldown == 0 and turn == False:
        mm_attack_br = True
    else:
        mm_attack_br = False
    if mr_bm_range == False and b_m_walk == False and m_r_walk == False and mr_cooldown == 0 and turn == False:
        mr_attack_bm = True
    else:
        mr_attack_bm = False
    if br_mr_range == False and b_r_walk == False and m_r_walk == False and mr_cooldown == 0 and turn == False:
        mr_attack_br = True
    else:
        mr_attack_br = False
    if bm_mr_range == False and b_m_walk == False and m_r_walk == False and bm_cooldown == 0 and turn == True:
        bm_attack_mr = True
    else:
        bm_attack_mr = False
    if br_mr_range == False and b_r_walk == False and m_r_walk == False and br_cooldown == 0 and turn == True:
        br_attack_mr = True
    else:
        br_attack_mr = False
    if bc_mm_range == False and b_c_walk == False and m_m_walk == False and bc_cooldown == 0 and turn == True:
        bc_attack_mm = True
    else:
        bc_attack_mm = False
    if bc_mm_range == False and b_c_walk == False and m_m_walk == False and mm_cooldown == 0 and turn == False:
        mm_attack_bc = True
    else:
        mm_attack_bc = False
    if bc_mr_range == False and b_c_walk == False and m_r_walk == False and bc_cooldown == 0 and turn == True:
        bc_attack_mr = True
    else:
        bc_attack_mr = False
    if mr_bc_range == False and b_c_walk == False and m_r_walk == False and mr_cooldown == 0 and turn == False:
        mr_attack_bc = True
    else:
        mr_attack_bc = False
    if bc_mc_range == False and b_c_walk == False and m_c_walk == False and bc_cooldown == 0 and turn == True:
        bc_attack_mc = True
    else:
        bc_attack_mc = False
    if bc_mc_range == False and b_c_walk == False and m_c_walk == False and mc_cooldown == 0 and turn == False:
        mc_attack_bc = True
    else:
        mc_attack_bc = False
    if mc_bm_range == False and b_m_walk == False and m_c_walk == False and mc_cooldown == 0 and turn == False:
        mc_attack_bm = True
    else:
        mc_attack_bm = False
    if mc_br_range == False and b_r_walk == False and m_c_walk == False and mc_cooldown == 0 and turn == False:
        mc_attack_br = True
    else:
        mc_attack_br = False
    if mc_bm_range == False and b_m_walk == False and m_c_walk == False and bm_cooldown == 0 and turn == True:
        bm_attack_mc = True
    else:
        bm_attack_mc = False
    if br_mc_range == False and b_r_walk == False and m_c_walk == False and br_cooldown == 0 and turn == True:
        br_attack_mc = True
    else:
        br_attack_mc = False

#deals damage to targets if possible
    if bm_attack_mm:
        b_m_sprite.update(b_m_coords, events, images["b_melee_2"])
        time.sleep(0.25)
        m_m_sprite.damage(20)
        bm_cooldown = 1
    if br_attack_mm:
        b_r_sprite.update(b_m_coords, events, images["b_ranged_2"])
        time.sleep(0.25)
        m_m_sprite.damage(20)
        bm_cooldown = 1
    if mm_attack_bm:
        m_m_sprite.update(m_m_coords, events, images["m_melee_2"])
        time.sleep(0.25)
        b_m_sprite.damage(20)
        mm_cooldown = 1
    if mm_attack_br:
        m_m_sprite.update(m_m_coords, events, images["m_melee_2"])
        time.sleep(0.25)
        b_r_sprite.damage(20)
        mm_cooldown = 1
    if mr_attack_bm:
        m_r_sprite.update(m_r_coords, events, images["m_ranged_2"])
        time.sleep(0.25)
        b_m_sprite.damage(20)
        mr_cooldown = 1
    if mr_attack_br:
        m_r_sprite.update(m_r_coords, events, images["m_ranged_2"])
        time.sleep(0.25)
        b_r_sprite.damage(20)
        mr_cooldown = 1
    if bm_attack_mr:
        b_m_sprite.update(b_m_coords, events, images["b_melee_2"])
        time.sleep(0.25)
        m_r_sprite.damage(20)
        bm_cooldown = 1
    if br_attack_mr:
        b_r_sprite.update(b_m_coords, events, images["b_ranged_2"])
        time.sleep(0.25)
        m_r_sprite.damage(20)
        br_cooldown = 1
    if bc_attack_mr:
        b_c_sprite.update(b_c_coords, events, images["b_cavalry_2"])
        time.sleep(0.25)
        m_r_sprite.damage(20)
        bc_cooldown = 1
    if bc_attack_mm:
        b_c_sprite.update(b_c_coords, events, images["b_cavalry_2"])
        time.sleep(0.25)
        m_m_sprite.damage(20)
        bc_cooldown = 1
    if bc_attack_mc:
        b_c_sprite.update(b_c_coords, events, images["b_cavalry_2"])
        time.sleep(0.25)
        m_c_sprite.damage(20)
        bc_cooldown = 1
    if mc_attack_bc:
        m_c_sprite.update(m_c_coords, events, images["m_cavalry_2"])
        time.sleep(0.25)
        b_c_sprite.damage(20)
        mc_cooldown = 1
    if mc_attack_bm:
        m_c_sprite.update(m_c_coords, events, images["m_cavalry_2"])
        time.sleep(0.25)
        b_m_sprite.damage(20)
        mc_cooldown = 1
    if mc_attack_br:
        m_c_sprite.update(m_c_coords, events, images["m_cavalry_2"])
        time.sleep(0.25)
        b_r_sprite.damage(20)
        mc_cooldown = 1
    if br_attack_mc:
        b_r_sprite.update(b_r_coords, events, images["b_ranged_2"])
        time.sleep(0.25)
        m_c_sprite.damage(20)
        br_cooldown = 1
    if mr_attack_bc:
        m_r_sprite.update(m_r_coords, events, images["m_ranged_2"])
        time.sleep(0.25)
        b_c_sprite.damage(20)
        mr_cooldown = 1
        #updates all sprites if no attacks
    else:
        b_m_sprite.update(b_m_coords, events, images["b_melee_2"])
        m_m_sprite.update(m_m_coords, events, images["m_melee_2"])
        b_r_sprite.update(b_r_coords, events, images["b_ranged_2"])
        m_r_sprite.update(m_r_coords, events, images["m_ranged_2"])
        b_c_sprite.update(b_c_coords, events, images["b_cavalry_2"])
        m_c_sprite.update(m_c_coords, events, images["m_cavalry_2"])


    # fill the screen with a background image
    screen.blit(images["gate_pa_bg"], (0, 0))

    group.draw(screen)# displays sprite

    
    if turn == True:
        turn_order = "British turn"

    elif turn == False:
        turn_order = "Māori turn"
    
    make_turn = "press spacebar to end turn"

#home screen code below
    if go == False:
       home_words_title = "Tales of Taranaki"
       home_screen_cover = pygame.draw.rect(screen, (0, 0, 0), [0, 0, 1500, 1500])
       home_words_subtitle = "(press space to start)"
       home_words_declaration = "A historically accurate game!*"
       home_words_moa_declaration = "*This game is historically accurete except for Māori riding Moa"
    
    else:
        home_words_title = ""
        home_words_subtitle = ""
        home_words_declaration = ""
        home_words_moa_declaration = ""

    home = title_font.render(home_words_title, True, (255, 255, 255) )
    screen.blit(home, (220, 264))

    home_subtitle = sub_font.render(home_words_subtitle, True, (255, 255, 255) )
    screen.blit(home_subtitle, (310, 400))

    home_declaration = sub_font.render(home_words_declaration, True, (255, 255, 255) )
    screen.blit(home_declaration, (250, 350))

    moa_declaration = sub_sub_font.render(home_words_moa_declaration, True, (255,255,255) )
    screen.blit(moa_declaration, (700,700))

    status_text = font.render(turn_order, True, (0, 0, 0))
    screen.blit(status_text, (20, 60))

    turn_instructions = font.render(make_turn, True, (0, 0, 0))
    screen.blit(turn_instructions, (20, 85))


    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(60)# limits FPS to 60
# quits game
pygame.quit()
