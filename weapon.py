import pygame
import constants
import math
import random

class Weapon():
    def __init__(self, image, bullet_image):
        self.original_image = image # when the weapon is changing direction
        self.direction = 0
        self.image = pygame.transform.rotate(self.original_image, self.direction)
        self.bullet_image = bullet_image
        self.rect = self.image.get_rect()
        self.fired = False
        self.last_shot = pygame.time.get_ticks()
    
    # def update(self, character):
    #     shot_cooldown = 500
    #     bullet = None
    #     self.rect.center = character.rect.center
        
    #     pos = pygame.mouse.get_pos()
    #     x_dist = pos[0] - self.rect.centerx
    #     y_dist = -(pos[1] - self.rect.centery)
    #     self.direction = math.degrees(math.atan2(y_dist, x_dist))

    #     if pygame.mouse.get_pressed()[0] and self.fired == False and (pygame.time.get_ticks() - self.last_shot) >= shot_cooldown:
    #         self.fired = True
    #         bullet = Bullet(self.rect.centerx, self.rect.centery, self.bullet_image, self.direction)
    #         self.last_shot = pygame.time.get_ticks()
        
    #     if pygame.mouse.get_pressed()[0] == False:
    #         self.fired = False
        
    #     return bullet
    
    def update(self, character):
        # if character.char_type == 0:
        #     shot_cooldown = 500
        # elif character.char_type == 1:
        #     shot_cooldown = 1000
        shot_cooldown = 500
        bullet = None
        self.rect.center = character.rect.center
        self.direction = character.direction + 90
        if character.char_type == 0:
            if pygame.mouse.get_pressed()[0] and self.fired == False and (pygame.time.get_ticks() - self.last_shot) >= shot_cooldown:
                self.fired = True
                bullet = Bullet(self.rect.centerx, self.rect.centery, self.bullet_image, self.direction)
                self.last_shot = pygame.time.get_ticks()
            
            if pygame.mouse.get_pressed()[0] == False:
                self.fired = False
        # if character.char_type == 1:
        #     if self.fired == False and (pygame.time.get_ticks() - self.last_shot) >= shot_cooldown:
        #         self.fired = True
        #         bullet = Bullet(self.rect.centerx, self.rect.centery, self.bullet_image, self.direction)
        #         self.last_shot = pygame.time.get_ticks()

        #         self.fired = False
        
        return bullet

    
    def draw(self, surface):
        self.image = pygame.transform.rotate(self.original_image, self.direction)
        # surface.blit(self.image, (self.rect.centerx - int(self.image.get_width()/2), self.rect.centery - int(self.image.get_height()/2)))
    

    
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, image, direction):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image
        self.direction = direction
        self.image = pygame.transform.rotate(self.original_image, self.direction)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.dx = math.cos(math.radians(self.direction)) * constants.BULLET_SPEED
        self.dy = -(math.sin(math.radians(self.direction)) * constants.BULLET_SPEED)

    def update(self, screen_scroll, obstacle_tiles, villain_list):
        damage = 0
        damage_text_pos = None
        
        self.rect.x += screen_scroll[0] + self.dx
        self.rect.y += screen_scroll[1] + self.dy

        for obstacle in obstacle_tiles:
            if obstacle[1].colliderect(self.rect):
                self.kill()
        
        if self.rect.right < 0 or self.rect.left > constants.SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > constants.SCREEN_HEIGHT:
            self.kill()
        
        for villain in villain_list:
            if villain.rect.colliderect(self.rect) and villain.alive:
                damage = 50 + random.randint(-5, 5)
                damage_text_pos = villain.rect
                villain.health -= damage
                self.kill()
                break
        
        return damage, damage_text_pos
    
    def draw(self, surface):
        surface.blit(self.image, (self.rect.centerx - int(self.image.get_width()/2), self.rect.centery - int(self.image.get_height()/2)))


class VillainBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, image, target_x, target_y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image
        self.direction = direction + 90
        x_dist = target_x - x
        y_dist = -(target_y - y)

        self.image = pygame.transform.rotate(self.original_image, self.direction)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.dx = math.cos(math.radians(self.direction)) * constants.VILLAIN_BULLET_SPEED
        self.dy = -(math.sin(math.radians(self.direction)) * constants.VILLAIN_BULLET_SPEED)

    def update(self, screen_scroll, obstacle_tiles, player):
        damage = 0
        damage_text_pos = None
        
        self.rect.x += screen_scroll[0] + self.dx
        self.rect.y += screen_scroll[1] + self.dy

        for obstacle in obstacle_tiles:
            if obstacle[1].colliderect(self.rect):
                self.kill()
        
        if self.rect.right < 0 or self.rect.left > constants.SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > constants.SCREEN_HEIGHT:
            self.kill()
        
        if player.rect.colliderect(self.rect) and player.alive:
            player.hit = True
            player.last_hit = pygame.time.get_ticks()
            damage = 30 + random.randint(-5, 5)
            damage_text_pos = player.rect
            player.health -= damage
            self.kill()
        
        return damage, damage_text_pos
    
    def draw(self, surface):
        surface.blit(self.image, (self.rect.centerx - int(self.image.get_width()/2), self.rect.centery - int(self.image.get_height()/2)))

