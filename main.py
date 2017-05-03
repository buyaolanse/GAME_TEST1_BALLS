# -*- coding: utf-8 -*- 

import pygame
import sys
import math
from pygame.locals import *
from random import *


#初始化
pygame.init()

#初始化mixer
pygame.mixer.init()

pygame.mixer.music.load('bg_music.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play()


dog_sound = pygame.mixer.Sound('dog.wav')
dog_sound.set_volume(0.2)

class Ball(pygame.sprite.Sprite):
    def __init__(self, image, position, speed, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()

        


        #球放在指定位置
        self.rect.left, self.rect.top = position
        self.speed = speed

        self.width, self.height = bg_size[0], bg_size[1]
        self.radius = self.rect.width/2

    def move(self):
        self.rect = self.rect.move(self.speed)

        if self.rect.right < 0:
            self.rect.left = self.width

        elif self.rect.left > self.width:
            self.rect.right = 0

        elif self.rect.bottom < 0:
            self.rect.top = self.height

        elif self.rect.top > self.height:
            self.rect.bottom = 0
        
class Glass(pygame.sprite.Sprite):
    def __init__(self, glass_image, bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.glass_image = pygame.image.load(glass_image).convert_alpha()
        self.glass_rect = self.glass_image.get_rect()


        self.glass_rect.left, self.glass_rect.top = (bg_size[0]-self.glass_rect.width)//2 ,\
                                                    bg_size[1] - self.glass_rect.height
        


        

def main():
    pygame.init()

    speed = [1,1]
    ball_image = 'grey_ball.png'
    bg_image = 'background.png'
    glass_image = 'glass.png'

    running = True

    #根据背景图片制定游戏界面尺寸

    bg_size = width, height = 1024, 681
    screen = pygame.display.set_mode(bg_size)
    pygame.display.set_caption('Play the ball - wc')

    background = pygame.image.load(bg_image).convert_alpha()


    #创建存放小球的列表
    balls = []
    group  = pygame.sprite.Group()
    
    #创建5个小球
    BALL_NUM = 5
    for i in range(BALL_NUM):
        #初始化小球，位置及速度均随机
        position = randint(0 , width-60), randint(0, height - 60)
        speed = [randint(-10,10), randint(-10,10)]
        print speed
        ball = Ball(ball_image, position, speed, bg_size)

        while pygame.sprite.spritecollide(ball, group, False, pygame.sprite.collide_circle):
            ball.rect.left, ball.rect.top = randint(0 , width-60), randint(0, height - 60)
            
        
        balls.append(ball)
        group.add(ball)


    #创建玻璃
    glass = Glass(glass_image, bg_size)

    clock = pygame.time.Clock()
    
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    dog_sound.play()



        screen.blit(background, (0,0))

        screen.blit(glass.glass_image, glass.glass_rect)
        

        for each in balls:
            each.move()
            screen.blit(each.image, each.rect)

#
        for each in group:
            group.remove(each)
            if pygame.sprite.spritecollide(each, group, False, pygame.sprite.collide_circle):
                each.speed[0] = -each.speed[0]
                each.speed[1] = -each.speed[1]

            group.add(each)


        pygame.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    main()
