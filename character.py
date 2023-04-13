import pygame
import constants
import math

class Character():
    def __init__(self, x, y, health, mob_animations, char_type):
        self.char_type = char_type
        self.score = 0
        self.direction = 0
        self.frame_index = 0
        self.action = 0 # 0: idle, 1: run
        self.animation_list = mob_animations[char_type]
        self.update_time = pygame.time.get_ticks()
        self.running = False
        self.health = health
        self.alive = True

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect(0, 0, constants.CHAR_SIZE * constants.SCALE, constants.CHAR_SIZE * constants.SCALE)
        self.rect.center = (x, y)
    
    def move(self, dx, dy):
        screen_scroll = [0, 0]

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
        self.rect.y += dy

        if self.char_type == 0:
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
        return screen_scroll

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