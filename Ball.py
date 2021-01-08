import pygame
import sys
import random

class Ball(pygame.sprite.Sprite):
    def __init__(self, redimage, greenimage, position, speed, bg_size):
        super().__init__()

        self.image = pygame.image.load(redimage).convert_alpha()
        self.fiximage = greenimage
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        self.speed = speed
        self.width, self.height = bg_size[0], bg_size[1]
        self.radius = self.rect.width / 2
        #用x，y记录坐标
        self.x = self.rect.left
        self.y = self.rect.top
        self.isfixed = False

    def move(self, group):
        #判断出界
        if self.rect.right <= 0:
            self.x = self.width
            if len(pygame.sprite.spritecollide(self, group, False, pygame.sprite.collide_circle)) == 1:
                self.x += self.speed[0]
                self.y += self.speed[1]
            else:
                self.x += self.rect.width
        elif self.rect.left >= self.width:
            self.x = -self.rect.width
            if len(pygame.sprite.spritecollide(self, group, False, pygame.sprite.collide_circle)) == 1:
                self.x += self.speed[0]
                self.y += self.speed[1]
            else:
                self.x -= self.rect.width
        elif self.rect.top >= self.height:
            self.y = -self.rect.height
            if len(pygame.sprite.spritecollide(self, group, False, pygame.sprite.collide_circle)) == 1:
                self.x += self.speed[0]
                self.y += self.speed[1]
            else:
                self.y -= self.rect.height
        elif self.rect.bottom <= 0:
            self.y = self.height
            if len(pygame.sprite.spritecollide(self, group, False, pygame.sprite.collide_circle)) == 1:
                self.x += self.speed[0]
                self.y += self.speed[1]
            else:
                self.y += self.rect.height
        else:
            self.x += self.speed[0]
            self.y += self.speed[1]

        #移动
        self.rect.left, self.rect.top = self.x, self.y

    def fix(self):
        self.image = pygame.image.load(self.fiximage).convert_alpha()
        self.isfixed = True