import pygame
import csv
from pygame import mixer
import constants
from character import Character
from weapon import Weapon
from weapon import Bullet
from items import Item
from world import World

# pygame setup
mixer.init()
pygame.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Shoot or Die")
clock = pygame.time.Clock()

level = 1
screen_scroll = [0, 0]

running = True
dt = 0
# player_direction = 0

# define player movement variables
moving_left = False
moving_right = False
moving_up = False
moving_down = False

font = pygame.font.Font("assets/fonts/zekton_rg.otf", 20)

#helper function to scale image
def scale_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w * scale, h * scale))

pygame.mixer.music.load("assets/audio/suspense.wav")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1, 0.0, 500)
shot_fx = pygame.mixer.Sound("assets/audio/shot_fx.wav")
shot_fx.set_volume(0.5)
hit_fx = pygame.mixer.Sound("assets/audio/hit_fx.wav")
hit_fx.set_volume(0.2)

life_empty = scale_img(pygame.image.load("assets/images/items/life_empty.png").convert_alpha(), constants.ITEM_SCALE)
life_half = scale_img(pygame.image.load("assets/images/items/life_half.png").convert_alpha(), constants.ITEM_SCALE)
life_full = scale_img(pygame.image.load("assets/images/items/life_full.png").convert_alpha(), constants.ITEM_SCALE)

coin_images = []
for x in range(4):
    img = scale_img(pygame.image.load(f"assets/images/items/coin_f{x}.png").convert_alpha(), constants.ITEM_SCALE)
    coin_images.append(img)

aid_images = []
for x in range(4):
    img = scale_img(pygame.image.load(f"assets/images/items/aid_f{x}.png").convert_alpha(), constants.ITEM_SCALE)
    aid_images.append(img)



def create_bullet():
    print("bullet created")

gun_image = pygame.image.load("assets/images/weapons/gun/0.png").convert_alpha()
bullet_image = pygame.image.load("assets/images/weapons/bullet.png").convert_alpha()

tile_list = []
for x in range(constants.TILE_TYPES):
    tile_image = pygame.image.load(f"assets/images/tiles/{x}.png").convert_alpha()
    tile_image = pygame.transform.scale(tile_image, (constants.TILE_SIZE, constants.TILE_SIZE))
    tile_list.append(tile_image)

mob_animations = []
mob_types = ["shooter", "villain"]
player_index = 0

animation_types = ["idle", "run"]

for mob in mob_types:
    animation_list = []
    for animation in animation_types:
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f"assets/images/characters/{mob}/{animation}/{i}.png").convert_alpha()
            temp_list.append(img)
        animation_list.append(temp_list)
    mob_animations.append(animation_list)

def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

def display_info():
    pygame.draw.rect(screen, constants.PANEL, (0, 0, constants.SCREEN_WIDTH, 50))
    pygame.draw.line(screen, constants.WHITE, (0, 50), (constants.SCREEN_WIDTH, 50))
    
    half_heart_drawn = False
    for i in range(5):
        if player.health >= ((i + 1) * 20):
            screen.blit(life_full, (10 + (i * 50), 0))
        elif (player.health % 20 > 0) and half_heart_drawn == False:
            screen.blit(life_half, (10 + (i * 50), 0))
            half_heart_drawn = True
        else:
            screen.blit(life_empty, (10 + (i * 50), 0))
    
    draw_text(f"X {player.score}", font, constants.WHITE, constants.SCREEN_WIDTH - 100, 15)

world_data = []
for row in range(constants.ROWS):
    r = [-1] * constants.COLS
    world_data.append(r)

with open(f"levels/level{level}_data.csv", newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter = ',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

world = World()
world.process_data(world_data, tile_list)


class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0
    
    def update(self):
        self.rect.y -= 1
        self.counter += 1
        if self.counter > 30:
            self.kill()


player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# create player
player = Character(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2, 70, mob_animations, player_index)
villain = Character(200, 300, 100, mob_animations, 1)
gun = Weapon(gun_image, bullet_image)

villain_list = []
villain_list.append(villain)

damage_text_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()

score_coin = Item(constants.SCREEN_WIDTH - 115, 23, 0, coin_images, True)
item_group.add(score_coin)

coin = Item(400, 400, 0, coin_images)
item_group.add(coin)
aid = Item(500, 200, 1, aid_images)
item_group.add(aid)

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
    
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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

    screen_scroll = player.move(dx, dy)
    print(screen_scroll)

    world.update(screen_scroll)
    for villain in villain_list:
        villain.update()
    player.update()
    
    bullet = gun.update(player)
    if bullet:
        bullet_group.add(bullet)
        shot_fx.play()

    for bullet in bullet_group:
        damage, damage_text_pos = bullet.update(villain_list)
        if damage:
            damage_text = DamageText(damage_text_pos.centerx, damage_text_pos.y, str(damage), constants.WHITE)
            damage_text_group.add(damage_text)
            hit_fx.play()
    damage_text_group.update()
    item_group.update(screen_scroll, player)

    world.draw(screen)

    player.draw(screen)
    
    for villain in villain_list:
        villain.draw(screen)
    
    gun.draw(screen)
    
    for bullet in bullet_group:
        bullet.draw(screen)
    
    damage_text_group.draw(screen)
    item_group.draw(screen)
    display_info()
    score_coin.draw(screen)

    pygame.display.flip()

    

pygame.quit()