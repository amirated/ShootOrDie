import pygame
import random

import csv
from pygame import mixer
import constants
from world import World
from character import Character
from weapon import Weapon
from weapon import Bullet
from items import Item
from button import Button

# pygame setup
mixer.init()
pygame.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Shoot or Die")
clock = pygame.time.Clock()

tip_of_the_session = constants.TIPS[random.randint(0, len(constants.TIPS) - 1)]
level = 7
start_game = False
pause_game = False
start_intro = False
level_complete = False
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

music_playing = False
death_fx_played = False
level_transition_shown = False
level_clear_fx_played = False

def play_music(music_label):
    print("play music " + music_label)
    # start_game_music
    # suspense
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    pygame.mixer.music.load(f"assets/audio/{music_label}.wav")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1, 0.0, 500)

shot_fx = pygame.mixer.Sound("assets/audio/shot_fx.wav")
shot_fx.set_volume(0.5)
hit_fx = pygame.mixer.Sound("assets/audio/hit_fx.wav")
hit_fx.set_volume(0.2)
death_fx = pygame.mixer.Sound("assets/audio/death_fx.wav")
death_fx.set_volume(0.8)
level_clear_fx = pygame.mixer.Sound("assets/audio/level_clear_fx.wav")
level_clear_fx.set_volume(0.8)

start_button_image = scale_img(pygame.image.load("assets/images/buttons/button_start.png").convert_alpha(), constants.SCALE_1)
exit_button_image = scale_img(pygame.image.load("assets/images/buttons/button_exit.png").convert_alpha(), constants.SCALE_1)
exit_button_image_white = scale_img(pygame.image.load("assets/images/buttons/button_exit_white.png").convert_alpha(), constants.SCALE_1)
restart_button_image = scale_img(pygame.image.load("assets/images/buttons/button_restart.png").convert_alpha(), constants.SCALE_1)
resume_button_image = scale_img(pygame.image.load("assets/images/buttons/button_resume.png").convert_alpha(), constants.SCALE_1)
controls_button_image = scale_img(pygame.image.load("assets/images/buttons/button_controls.png").convert_alpha(), constants.SCALE_1)
continue_button_image = scale_img(pygame.image.load("assets/images/buttons/button_continue_white.png").convert_alpha(), constants.SCALE_1)

menu_background_image = pygame.image.load("assets/images/menu_background_image.png")
pause_background_image = pygame.image.load("assets/images/pause_background_image.png")
game_over_background_image = pygame.image.load("assets/images/game_over_background_image.png")

life_empty = scale_img(pygame.image.load("assets/images/items/life_empty.png").convert_alpha(), constants.SCALE_3)
life_half = scale_img(pygame.image.load("assets/images/items/life_half.png").convert_alpha(), constants.SCALE_3)
life_full = scale_img(pygame.image.load("assets/images/items/life_full.png").convert_alpha(), constants.SCALE_3)

villain_image = scale_img(pygame.image.load(f"assets/images/characters/villain/idle/0.png").convert_alpha(), constants.SCALE_1)
trophy_image = scale_img(pygame.image.load(f"assets/images/items/trophy_image.png").convert_alpha(), constants.SCALE_2)

coin_images = []
for x in range(4):
    img = scale_img(pygame.image.load(f"assets/images/items/coin_f{x}.png").convert_alpha(), constants.SCALE_3)
    coin_images.append(img)

aid_images = []
for x in range(4):
    img = scale_img(pygame.image.load(f"assets/images/items/aid_f{x}.png").convert_alpha(), constants.SCALE_3)
    aid_images.append(img)

blaze_images = []
for x in range(4):
    img = scale_img(pygame.image.load(f"assets/images/items/blaze_f{x}.png").convert_alpha(), constants.SCALE_2)
    blaze_images.append(img)

flagger_images = []
for x in range(4):
    img = scale_img(pygame.image.load(f"assets/images/items/flagger_f{x}.png").convert_alpha(), constants.SCALE_2)
    flagger_images.append(img)

item_images = []
item_images.append(coin_images)
item_images.append(aid_images)
item_images.append(blaze_images)
item_images.append(flagger_images)

gun_image = pygame.image.load("assets/images/weapons/gun/0.png").convert_alpha()
bullet_image = pygame.image.load("assets/images/weapons/bullet.png").convert_alpha()
villain_bullet_image = pygame.image.load("assets/images/weapons/villain_bullet.png").convert_alpha()

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
            img = scale_img(pygame.image.load(f"assets/images/characters/{mob}/{animation}/{i}.png").convert_alpha(), constants.SCALE_2)
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
    
    draw_text("LEVEL: " + str(level), font, constants.WHITE, constants.SCREEN_WIDTH / 2, 15)

    draw_text(f"X {len(world.villain_list)}", font, constants.WHITE, constants.SCREEN_WIDTH - 200, 15)
    draw_text(f"X {player.score}", font, constants.WHITE, constants.SCREEN_WIDTH - 100, 15)

def display_controls():
    pygame.draw.rect(screen, constants.BLACK, (100, 100, constants.SCREEN_WIDTH - 200, 250))
    draw_text("Player controls:", font, constants.WHITE, 120, 120)
    draw_text("MOVE: W, A, S, D", font, constants.WHITE, 140, 145)
    draw_text("SHOOT: Mouse Left", font, constants.WHITE, 140, 170)
    draw_text("PAUSE: ESC", font, constants.WHITE, 140, 195)
    draw_text(f"TIP: {tip_of_the_session}", font, constants.WHITE, 120, 300)

def show_message(message):
    pygame.draw.rect(screen, constants.WHITE, (200, 150, constants.SCREEN_WIDTH - 400, 100))
    draw_text(message, font, constants.BLACK, 220, 170)
    # draw_text(message, font, constants.BLACK, 220, 200)

def show_dialog_box(message):
    continue_button = None
    exit_button_white = None
    
    pygame.draw.rect(screen, constants.WHITE, (200, 100, constants.SCREEN_WIDTH - 400, 180))
    for i in range(len(message["messages"])):
        draw_text(message["messages"][i], font, constants.BLACK, 230, 120 + (i * 25))
    if message["new_item"] == "COINS":
        screen.blit(coin_images[0], (230, 200))
        draw_text(message["new_item_description"], font, constants.BLACK, 270, 200)
    if message["new_item"] == "AID":
        screen.blit(aid_images[0], (230, 200))
        draw_text(message["new_item_description"], font, constants.BLACK, 270, 200)
    if message["new_item"] == "BLAZE":
        screen.blit(blaze_images[0], (230, 200))
        draw_text(message["new_item_description"], font, constants.BLACK, 270, 200)
    if message["new_item"] == "FLAGGER":
        screen.blit(flagger_images[0], (230, 200))
        draw_text(message["new_item_description"], font, constants.BLACK, 270, 200)
    if message["new_item"] == "TROPHY":
        screen.blit(trophy_image, (220, 200))
        draw_text(message["new_item_description"], font, constants.BLACK, 300, 220)
        
    if level == constants.FINAL_LEVEL:
        exit_button_white = Button(constants.SCREEN_WIDTH // 2 - 100, constants.SCREEN_HEIGHT // 2 - 0, exit_button_image_white)
    else:
        continue_button = Button(constants.SCREEN_WIDTH // 2 - 100, constants.SCREEN_HEIGHT // 2 - 0, continue_button_image)
    return continue_button, exit_button_white

def reset_level():
    level_transition_shown = False
    death_fx_played = False
    play_music('suspense')
    damage_text_group.empty()
    bullet_group.empty()
    villain_bullet_group.empty()
    item_group.empty()
    w_data = []
    for row in range(constants.ROWS):
        r = [-1] * constants.COLS
        w_data.append(r)
    return w_data


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
world.process_data(world_data, tile_list, item_images, mob_animations)


class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0
    
    def update(self):
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]
        
        self.rect.y -= 1
        self.counter += 1
        if self.counter > 30:
            self.kill()


class ScreenTransition():
    def __init__(self, direction, color, speed):
        self.direction = direction
        self.color = color
        self.speed = speed
        self.fade_counter = 0
    
    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1: # horizontal
            pygame.draw.rect(screen, self.color, (0 - self.fade_counter, 0, constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.color, (constants.SCREEN_WIDTH // 2 + self.fade_counter, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        elif self.direction == 2: # vertical
            pygame.draw.rect(screen, self.color, (0, 0, constants.SCREEN_WIDTH, self.fade_counter))

        if self.fade_counter >= constants.SCREEN_WIDTH:
            fade_complete = True
        return fade_complete

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# create player
player = world.player
gun = Weapon(gun_image, bullet_image)

villain_list = world.villain_list

damage_text_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
villain_bullet_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()

# x, y, health, mob_animations, char_type, boss, size, villain_list

score_coin = Item(constants.SCREEN_WIDTH - 115, 23, 0, coin_images, True)
item_group.add(score_coin)

for item in world.item_list:
    item_group.add(item)

intro_fade = ScreenTransition(1, constants.BLACK, 40)
death_fade = ScreenTransition(2, constants.BLACK, 40)

start_button = Button(constants.SCREEN_WIDTH // 2 - 100, constants.SCREEN_HEIGHT // 2 - 100, start_button_image)
restart_button = Button(constants.SCREEN_WIDTH // 2 - 100, constants.SCREEN_HEIGHT // 2 - 0, restart_button_image)
resume_button = Button(constants.SCREEN_WIDTH // 2 - 100, constants.SCREEN_HEIGHT // 2 - 100, resume_button_image)
controls_button = Button(constants.SCREEN_WIDTH // 2 - 100, constants.SCREEN_HEIGHT // 2 - 0, controls_button_image)
exit_button = Button(constants.SCREEN_WIDTH // 2 - 100, constants.SCREEN_HEIGHT // 2 + 100, exit_button_image)

while running:

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(constants.FPS) / 1000
    if start_game == False:
        if music_playing == False:
            play_music('start_game_music')
            music_playing = True
        screen.blit(menu_background_image, (0, 0))
        if start_button.draw(screen):
            start_game = True
            start_intro = True
            music_playing = False
        if controls_button.draw(screen):
            display_controls()
        if exit_button.draw(screen):
            running = False
            music_playing = False
    else:
        if pause_game == True:
            screen.blit(pause_background_image, (0, 0))
            if resume_button.draw(screen):
                play_music('suspense')
                pause_game = False
            if controls_button.draw(screen):
                display_controls()
            if exit_button.draw(screen):
                running = False
        else:
            if music_playing == False:
                play_music('suspense')
                music_playing = True

            screen.fill(constants.BG)
            
            if player.alive:
                if level_complete == True and level_transition_shown == False:
                    if level_clear_fx_played == False:
                        pygame.mixer.music.stop()
                        level_clear_fx.play()
                        level_clear_fx_played = True
                else:
                    # calculate player movement
                    dx = 0
                    dy = 0
                    
                    if moving_right == True:
                        dx = (constants.SPEED + player.speed_mod)
                    if moving_left == True:
                        dx = -(constants.SPEED + player.speed_mod)
                    if moving_up == True:
                        dy = -(constants.SPEED + player.speed_mod)
                    if moving_down == True:
                        dy = (constants.SPEED + player.speed_mod)
                

                    screen_scroll, level_complete, display_message = player.move(dx, dy, world.obstacle_tiles, world.exit_tile)
                    
                    world.update(screen_scroll)
                    for villain in villain_list:
                        villain_bullet = villain.ai(player, world.obstacle_tiles, screen_scroll, villain_bullet_image)
                        # villain_bullet = gun.update(villain)
                        if villain.alive:
                            villain.update()
                            if villain_bullet:
                                villain_bullet_group.add(villain_bullet)
                                shot_fx.play()
                        else:
                            villain_list.remove(villain)
                            # villain.kill()

                    player.update()
                    
                    bullet = gun.update(player)
                    if bullet:
                        bullet_group.add(bullet)
                        shot_fx.play()

                    for bullet in bullet_group:
                        damage, damage_text_pos = bullet.update(screen_scroll, world.obstacle_tiles, villain_list)
                        if damage:
                            damage_text = DamageText(damage_text_pos.centerx, damage_text_pos.y, str(damage), constants.WHITE)
                            damage_text_group.add(damage_text)
                            hit_fx.play()
                
                    for villain_bullet in villain_bullet_group:
                        damage, damage_text_pos = villain_bullet.update(screen_scroll, world.obstacle_tiles, player)
                        if damage:
                            damage_text = DamageText(damage_text_pos.centerx, damage_text_pos.y, str(damage), constants.WHITE)
                            damage_text_group.add(damage_text)
                            hit_fx.play()
                    damage_text_group.update()
                    item_group.update(screen_scroll, player)

            # draw stuff
            world.draw(screen)
            player.draw(screen)
            
            for villain in villain_list:
                villain.draw(screen)
            
            gun.draw(screen)
            
            for bullet in bullet_group:
                bullet.draw(screen)
            
            for villain_bullet in villain_bullet_group:
                villain_bullet.draw(screen)
            
            damage_text_group.draw(screen)
            item_group.draw(screen)
            display_info()
            score_coin.draw(screen)
            screen.blit(villain_image, (constants.SCREEN_WIDTH - 240, 10))
            if display_message:
                show_message(display_message)
            
            if level_complete == True and level_transition_shown == False:
                continue_button, exit_button_white = show_dialog_box(constants.LEVEL_CLEAR_MESSAGE[level - 1])
                if not exit_button_white == None:
                    if exit_button_white.draw(screen):
                        running = False 
                if not continue_button == None:
                    if continue_button.draw(screen):
                        level_transition_shown = True

            if level_complete == True and level_transition_shown == True:
                start_intro = True
                level += 1
                # show level transition screen
                
                world_data = reset_level()
                # level_complete = False
                with open(f"levels/level{level}_data.csv", newline="") as csvfile:
                    reader = csv.reader(csvfile, delimiter = ',')
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)

                world = World()
                world.process_data(world_data, tile_list, item_images, mob_animations)
                temp_health = player.health
                temp_score = player.score
                player = world.player
                player.health = temp_health
                player.score = temp_score

                villain_list = world.villain_list
                score_coin = Item(constants.SCREEN_WIDTH - 115, 23, 0, coin_images, True)
                item_group.add(score_coin)

                for item in world.item_list:
                    item_group.add(item)

            if start_intro == True:
                if intro_fade.fade():
                    start_intro = False
                    intro_fade.fade_counter = 0

            if player.alive == False:
                if death_fx_played == False:
                    death_fx.play()
                    death_fx_played = True
                    play_music('game_over_music')
                if death_fade.fade():
                    screen.blit(game_over_background_image, (0, 0))
                    if restart_button.draw(screen):
                        death_fade.fade_counter = 0
                        start_intro = True
                        world_data = reset_level()
                        # level_complete = False
                        with open(f"levels/level{level}_data.csv", newline="") as csvfile:
                            reader = csv.reader(csvfile, delimiter = ',')
                            for x, row in enumerate(reader):
                                for y, tile in enumerate(row):
                                    world_data[x][y] = int(tile)

                        world = World()
                        world.process_data(world_data, tile_list, item_images, mob_animations)
                        temp_score = player.score
                        player = world.player
                        player.score = temp_score

                        villain_list = world.villain_list
                        score_coin = Item(constants.SCREEN_WIDTH - 115, 23, 0, coin_images, True)
                        item_group.add(score_coin)

                        for item in world.item_list:
                            item_group.add(item)
                    if exit_button.draw(screen):
                        running = False

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
            if event.key == pygame.K_ESCAPE:
                pause_game = True
                play_music('pause_music')
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                moving_up = False
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_s:
                moving_down = False
            if event.key == pygame.K_d:
                moving_right = False
    
    pygame.display.flip()

    

pygame.quit()