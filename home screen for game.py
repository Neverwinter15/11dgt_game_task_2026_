import pygame

# pygame setup
pygame.init()
# makes game full screen
screen = pygame.display.set_mode((1000,800))
clock = pygame.time.Clock()
running = True
font = pygame.font.Font(None, 100)
sub_font = pygame.font.Font(None, 50)
sub_sub_font = pygame.font.Font(None, 10)
home_screen = True
#variables to help recoard if a sprite has been clicked and cords
sprite_clicked = False
next_coordinates = None

def on_click():
    global sprite_clicked
    sprite_clicked = True  

class ClickableSprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y, callback):
        super().__init__()
        self.image = image
        self.image.fill((255, 0, 0)) 
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.callback = callback

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.callback()
                    return True 
        return False


sprite = ClickableSprite(pygame.Surface((100, 100)), 50, 50, on_click)
group = pygame.sprite.GroupSingle(sprite)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            
        
        if event.type == pygame.MOUSEBUTTONDOWN and sprite_clicked:# checks if sprite is clicked and mouse is clicked
           
            if not sprite.rect.collidepoint(event.pos): 
                next_coordinates = event.pos 
                sprite_clicked = False
    
   # home_screen_cover = pygame.draw.rect(screen, (0, 0, 0), [0, 0, 1500, 1500])
   # home_screen = font.render("Welcome to the Tales of Tarinaki", True, (255, 255, 255))
   # screen.blit(home_screen, (628, 221))

    #shuts down the game when k button is pressed


    
    sprite.update(events)

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
    else:# tells you to click
        status_str = "click to start."
    
    status_text = font.render(status_str, True, (0, 0, 0))
    screen.blit(status_text, (100, 100))
    home_screen_cover = True
    
    if home_screen == True:
       home_words_title = "Tales of Tarinaki"
       home_screen_cover = pygame.draw.rect(screen, (0, 0, 0), [0, 0, 1500, 1500])
       home_words_subtitle = "(press space to start)"
       home_words_declaration = "A historically accurate game!*"
       home_words_moa_declaration = "*This game is historically accurete except for Māori riding Moa"
    home = font.render(home_words_title, True, (255, 255, 255) )
    screen.blit(home, (220, 264))

    home_subtitle = sub_font.render(home_words_subtitle, True, (255, 255, 255) )
    screen.blit(home_subtitle, (310, 400))

    home_declaration = sub_font.render(home_words_declaration, True, (255, 255, 255) )
    screen.blit(home_declaration, (250, 350))

    moa_declaration = sub_sub_font.render(home_words_moa_declaration, True, (255,255,255) )
    screen.blit(moa_declaration, (700,700))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False
    if keys[pygame.K_SPACE]:
        home_screen = False
        home_words_title = ""
        home_words_subtitle = ""
        home_words_declaration = ""
        home_words_moa_declaration = ""
    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(60)# limits FPS to 60

# quits game
pygame.quit()