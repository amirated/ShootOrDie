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
    
    def update(self, player):
        shot_cooldown = 500
        bullet = None
        self.rect.center = player.rect.center
        
        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - self.rect.centerx
        y_dist = -(pos[1] - self.rect.centery)
        self.direction = math.degrees(math.atan2(y_dist, x_dist))

        if pygame.mouse.get_pressed()[0] and self.fired == False and (pygame.time.get_ticks() - self.last_shot) >= shot_cooldown:
            self.fired = True
            bullet = Bullet(self.rect.centerx, self.rect.centery, self.bullet_image, self.direction)
            self.last_shot = pygame.time.get_ticks()
        
        if pygame.mouse.get_pressed()[0] == False:
            self.fired = False
        
        return bullet

    
    def draw(self, surface):
        self.image = pygame.transform.rotate(self.original_image, self.direction)
        surface.blit(self.image, (self.rect.centerx - int(self.image.get_width()/2), self.rect.centery - int(self.image.get_height()/2)))
    

    
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

    def update(self, villain_list):
        damage = 0
        damage_text_pos = None
        
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.right < 0 or self.rect.left > constants.SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > constants.SCREEN_HEIGHT:
            self.kill()
        
        for villain in villain_list:
            if villain.rect.colliderect(self.rect) and villain.alive:
                damage = 10 + random.randint(-5, 5)
                damage_text_pos = villain.rect
                villain.health -= damage
                self.kill()
                break
        
        return damage, damage_text_pos
    
    def draw(self, surface):
        surface.blit(self.image, (self.rect.centerx - int(self.image.get_width()/2), self.rect.centery - int(self.image.get_height()/2)))

