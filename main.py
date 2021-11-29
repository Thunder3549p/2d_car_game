import pygame
from pygame.locals import *
import random
import sys
import time

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (80, 80, 80)

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
SPEED = 5
SCORE = 0

font = pygame.font.Font("game_over.ttf", 80)
font_small = pygame.font.Font("game_over.ttf", 36)
game_over = font.render("Game Over", True, WHITE)

background = pygame.image.load("AnimatedStreet.png")

DISPLAYSURF = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))
DISPLAYSURF.fill(GREY)
pygame.display.set_caption("CAR GAME")
pygame.mixer.music.load("background.wav")
pygame.mixer.music.play(3)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > 600:
            SCORE +=1
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0)

class Enemy2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy-2.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > 600:
            SCORE +=1
            self.rect.top = 0
            self.rect.center = (random.randint(15, 185), 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def update(self):
        pass
        # if pressed_keys[K_UP]:
        # self.rect.move_ip(0, -5)
        # if pressed_keys[K_DOWN]:
        # self.rect.move_ip(0,10)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > -100:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-10, 0)
        if self.rect.right < 800:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(10, 0)


class Background():
    def __init__(self):
        self.bgimage = pygame.image.load('AnimatedStreet.png')
        self.rectBGimg = self.bgimage.get_rect()

        self.bgY1 = 0
        self.bgX1 = 0

        self.bgY2 = self.rectBGimg.height
        self.bgX2 = 0

        self.movingUpSpeed = 5

    def update(self):
        self.bgY1 -= self.movingUpSpeed
        self.bgY2 -= self.movingUpSpeed
        if self.bgY1 <= -self.rectBGimg.height:
            self.bgY1 = self.rectBGimg.height
        if self.bgY2 <= -self.rectBGimg.height:
            self.bgY2 = self.rectBGimg.height

    def render(self):
        DISPLAYSURF.blit(self.bgimage, (self.bgX1, self.bgY1))
        DISPLAYSURF.blit(self.bgimage, (self.bgX2, self.bgY2))

P1 = Player()
E1 = Enemy()

back_ground = Background()
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(E1)
all_sprites.add(P1)

INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 1

        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    back_ground.update()
    back_ground.render()

    scores = font_small.render(str(SCORE), True, WHITE)
    score_title = font_small.render("SCORE-", True, WHITE)
    DISPLAYSURF.blit(score_title, (10,10))
    DISPLAYSURF.blit(scores, (60, 10))

    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

        if pygame.sprite.spritecollideany(P1, enemies):
            pygame.mixer.music.stop()
            pygame.mixer.Sound("crash.wav").play()
            time.sleep(1)

            DISPLAYSURF.fill(BLACK)
            DISPLAYSURF.blit(game_over, (125, 250))
            DISPLAYSURF.blit(scores, (210, 320))
            DISPLAYSURF.blit(score_title, (160, 320))

            pygame.display.update()
            for entity in all_sprites:
                entity.kill()
                time.sleep(5)
                pygame.quit()
                sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)
