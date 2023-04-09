# Example file showing a circle moving on screen
import pygame
import constants
from character import Character

# pygame setup
pygame.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Shoot or Die")
clock = pygame.time.Clock()
running = True
dt = 0

# define player movement variables
moving_left = False
moving_right = False
moving_up = False
moving_down = False

#helper function to scale image
def scale_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w * scale, h * scale))

animation_types = ["idle", "run"]

animation_list = []
for animation in animation_types:
    temp_list = []
    for i in range(4):
        img = pygame.image.load(f"assets/images/characters/shooter/{animation}/{i}.png").convert_alpha()
        temp_list.append(img)
    animation_list.append(temp_list)

# player_image = 
# player_image = scale_img(player_image, constants.SCALE)


player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# create player
player = Character(100, 100, animation_list, 0)

while running:

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(constants.FPS) / 1000

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(constants.BG)

    # calculate player movement
    dx = 0
    dy = 0
    
    if moving_right == True:
        dx = constants.SPEED
    if moving_left == True:
        dx = -constants.SPEED
    if moving_up == True:
        dy = -constants.SPEED
    if moving_down == True:
        dy = constants.SPEED
    
    # move player
    player.move(dx, dy)

    player.update()
    
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # take keyboard presses

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                moving_up = True
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_s:
                moving_down = True
            if event.key == pygame.K_d:
                moving_right = True
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                moving_up = False
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_s:
                moving_down = False
            if event.key == pygame.K_d:
                moving_right = False

    # pygame.draw.circle(screen, "red", player_pos, 40)
    player.draw(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

    

pygame.quit()