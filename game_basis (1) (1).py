import pygame
import random

# initialize pygame and create a full-screen display
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True

# helper function to get a random blue circle position inside the screen
def get_random_blue_position(radius):
    return pygame.Vector2(
        random.randint(radius, screen.get_width() - radius),
        random.randint(radius, screen.get_height() - radius),
    )

# red player circle settings and starting position at screen center
player_radius = 40
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# blue circle settings and initial random spawn
blue_radius = 40
blue_speed = 5
blue_pos = get_random_blue_position(blue_radius)

# Boolean to check whether red is visible or not.
red_visible = True

# make sure the blue circle does not spawn on top of the red circle
while blue_pos.distance_to(player_pos) < player_radius + blue_radius + 10:
    blue_pos = get_random_blue_position(blue_radius)

# main game loop
while running:
    # process all pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # read keyboard state
    keys = pygame.key.get_pressed()

    # close game when ESC is pressed
    if keys[pygame.K_ESCAPE]:
        running = False

    # move the blue circle with arrow keys
    if keys[pygame.K_LEFT]:
        blue_pos.x -= blue_speed
    if keys[pygame.K_RIGHT]:
        blue_pos.x += blue_speed
    if keys[pygame.K_UP]:
        blue_pos.y -= blue_speed
    if keys[pygame.K_DOWN]:
        blue_pos.y += blue_speed

    # keep blue circle inside the screen boundaries
    blue_pos.x = max(blue_radius, min(blue_pos.x, screen.get_width() - blue_radius))
    blue_pos.y = max(blue_radius, min(blue_pos.y, screen.get_height() - blue_radius))

    # determine whether the blue circle is near the red circle
    proximity_distance = blue_pos.distance_to(player_pos)

    # Red diseappers when in proximity to blue, but reappears when blue moves away.
    red_visible = proximity_distance > 50 + player_radius

    #If you want the red circle to disappear, then use the following:
    # if proximity_distance <= 50 + player_radius:
    #     red_visible = False

    # clear the screen with a solid background color
    screen.fill("green")

    # draw the red circle only when it is not within proximity
    if red_visible:
        pygame.draw.circle(screen, "red", player_pos, player_radius)

    pygame.draw.circle(screen, "blue", blue_pos, blue_radius)

    # update the display to show the new frame
    pygame.display.flip()

    # cap the frame rate at 60 FPS
    clock.tick(60)

# clean up pygame resources when exiting
pygame.quit()