import pygame
import weapon
import constants
import math

class Character():
    def __init__(self, x, y, health, mob_animations, char_type, boss, size, villain_list):
        self.char_type = char_type
        self.boss = boss
        self.score = 0
        self.direction = 0
        self.speed_mod = 0
        self.speed_mod_update_time = pygame.time.get_ticks()
        self.frame_index = 0
        self.action = 0 # 0: idle, 1: run
        self.animation_list = mob_animations[char_type]
        self.world_villain_list = villain_list
        self.update_time = pygame.time.get_ticks()
        self.running = False
        self.health = health
        self.alive = True
        self.hit = False
        self.last_hit = pygame.time.get_ticks()
        self.last_attack = pygame.time.get_ticks()

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect(0, 0, constants.CHAR_SIZE * size, constants.CHAR_SIZE * size)
        self.rect.center = (x, y)
    
    
    def move(self, dx, dy, obstacle_tiles, exit_tile = None):
        screen_scroll = [0, 0]
        level_complete = False
        display_message = None

        self.running = False
        #control diagonal speed
        if dx != 0 or dy != 0:
            self.running = True
        
        if dx != 0 and dy != 0:
            dx = dx * constants.DIAGONAL_COEFFICIENT
            dy = dy * constants.DIAGONAL_COEFFICIENT
            if dx > 0 and dy < 0:
                self.direction = 315
            elif dx > 0 and dy > 0:
                self.direction = 225
            elif dx < 0 and dy > 0:
                self.direction = 135
            elif dx < 0 and dy < 0:
                self.direction = 45
        else:
            if dy > 0:
                self.direction = 180
            elif dy < 0:
                self.direction = 0
            elif dx > 0:
                self.direction = 270
            elif dx < 0:
                self.direction = 90
        
        self.rect.x += dx
        for obstacle in obstacle_tiles:
            if obstacle[1].colliderect(self.rect):
                if dx > 0:
                    self.rect.right = obstacle[1].left
                if dx < 0:
                    self.rect.left = obstacle[1].right

        self.rect.y += dy
        for obstacle in obstacle_tiles:
            if obstacle[1].colliderect(self.rect):
                if dy > 0:
                    self.rect.bottom = obstacle[1].top
                if dy < 0:
                    self.rect.top = obstacle[1].bottom
        
        if self.char_type == 0:
            if exit_tile[1].colliderect(self.rect):
                exit_distance = math.sqrt(((self.rect.centerx - exit_tile[1].centerx) ** 2) + ((self.rect.centery - exit_tile[1].centery) ** 2))
                if exit_distance < 20:
                    if len(self.world_villain_list) > 0:
                        display_message = "Portal locked! Destroy all villains to unlock this portal."
                    else:
                        level_complete = True
            if self.rect.right > (constants.SCREEN_WIDTH - constants.SCROLL_THRESH_X):
                screen_scroll[0] = (constants.SCREEN_WIDTH - constants.SCROLL_THRESH_X) - self.rect.right
                self.rect.right = constants.SCREEN_WIDTH - constants.SCROLL_THRESH_X
            if self.rect.left < constants.SCROLL_THRESH_X:
                screen_scroll[0] = constants.SCROLL_THRESH_X - self.rect.left
                self.rect.left = constants.SCROLL_THRESH_X
        
            if self.rect.bottom > (constants.SCREEN_HEIGHT - constants.SCROLL_THRESH_Y):
                screen_scroll[1] = (constants.SCREEN_HEIGHT - constants.SCROLL_THRESH_Y) - self.rect.bottom
                self.rect.bottom = constants.SCREEN_HEIGHT - constants.SCROLL_THRESH_Y
            if self.rect.top < constants.SCROLL_THRESH_Y:
                screen_scroll[1] = constants.SCROLL_THRESH_Y - self.rect.top
                self.rect.top = constants.SCROLL_THRESH_Y
        return screen_scroll, level_complete, display_message
    
    def ai(self, player, obstacle_tiles, screen_scroll, villain_bullet_image):
        clipped_line = ()
        ai_dx = 0
        ai_dy = 0
        villain_bullet = None
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        line_of_sight = ((self.rect.centerx, self.rect.centery), (player.rect.centerx, player.rect.centery))
        for obstacle in obstacle_tiles:
            if obstacle[1].clipline(line_of_sight):
                clipped_line = obstacle[1].clipline(line_of_sight)

        distance = math.sqrt(((self.rect.centerx - player.rect.centerx) ** 2) + ((self.rect.centerx - player.rect.centerx) ** 2))
        if not clipped_line and distance > constants.NEAR_RANGE and distance < constants.FAR_RANGE:
            if self.rect.centerx > player.rect.centerx:
                ai_dx = -constants.VILLAIN_SPEED
            if self.rect.centerx < player.rect.centerx:
                ai_dx = constants.VILLAIN_SPEED
            if self.rect.centery > player.rect.centery:
                ai_dy = -constants.VILLAIN_SPEED
            if self.rect.centery < player.rect.centery:
                ai_dy = constants.VILLAIN_SPEED
        if self.alive:
            self.move(ai_dx, ai_dy, obstacle_tiles)
            villain_bullet_cooldown = 1000
            if not clipped_line and distance < constants.FAR_RANGE:
                if pygame.time.get_ticks() - self.last_attack >= villain_bullet_cooldown:
                    villain_bullet = weapon.VillainBullet(self.rect.centerx, self.rect.centery, villain_bullet_image, player.rect.centerx, player.rect.centery, self.direction)
                    self.last_attack = pygame.time.get_ticks()
        return villain_bullet


    def update(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False
        
        # check player action
        if self.running == True:
            self.update_action(1) # run
        else:
            self.update_action(0) # idle
        animation_cooldown = 70
        # handle animation
        # update image
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
        
        # update to remove speed boost
        speed_mod_expiry = 9000
        if not self.speed_mod == 0:
            if pygame.time.get_ticks() - self.speed_mod_update_time > speed_mod_expiry:
                self.speed_mod = 0
                self.speed_mod_update_time = pygame.time.get_ticks()


    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            # update animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        direction_image = pygame.transform.rotate(self.image, self.direction)
        if self.char_type == 0:
            if self.direction in [45, 135, 225, 315] :
                surface.blit(direction_image, (self.rect.x - constants.SHOOTER_DIAG_OFFSET, self.rect.y - constants.SHOOTER_DIAG_OFFSET))
            else:
                surface.blit(direction_image, (self.rect.x, self.rect.y))
            # surface.blit(direction_image, self.rect)
        else:
            surface.blit(direction_image, self.rect)
        pygame.draw.rect(surface, constants.RED, self.rect, 1)
        # print(self.direction)