import pygame
from pygame import mixer
import random
import math


# iinitialize pygame
pygame.init()

# Screen Created
screen = pygame.display.set_mode((800, 600))

# Add background Img
background = pygame.image.load('background.png')

#Background Music
mixer.music.load('backmusic.wav')
mixer.music.play(-1)

# Title and Icon(aslo put .png)
pygame.display.set_caption("Space Inavder - By Deep Kadakia")
Icon = pygame.image.load('icon.png')
pygame.display.set_icon(Icon)

# Player
shooterImg = pygame.image.load('player.png')
shooterX = 370
shooterY = 480
shooterX_change = 0
shooterY_change = 0

# Alien
alienImg = []
alienX = []
alienY = []
alienX_change = []
alienY_change = []
num_of_alien = 6

for j in range(num_of_alien):
    alienImg.append(pygame.image.load('alien.png'))
    alienX.append(random.randint(50, 735))
    alienY.append(random.randint(40, 170))
    alienX_change.append(2)
    alienY_change.append(40)

# Bullet
# Ready --> You cant see the bullet on screen
# Fire-->  The buullet is currently moving

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 15
bullet_state = "ready"

#SCORE

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 15
textY = 15

#Game_Over
game_over = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x,y):
    score = font.render("Score:" + str(score_value), True, (255,255,255))
    screen.blit(score, (x,y))

def game_over_text():
    over_text = game_over.render("GAME OVER" ,True, (255, 255, 255))
    screen.blit(over_text, (200,250))


def shooter(X, Y):
    screen.blit(shooterImg, (X, Y))


def alien(X, Y, j):
    screen.blit(alienImg[j], (X, Y))


def fire_bullet(X, Y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (X + 16, Y + 10))


def isCollision(alienX, alienY, bulletX, bulletY):
    distance = math.sqrt((math.pow(alienX - bulletX, 2)) + (math.pow(alienY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# screen timing
screen_run = True
while screen_run:

    # RGB = Red, Gree, Blue
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            screen_run = False

        # For Keys pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                shooterX_change = -5.5
            if event.key == pygame.K_RIGHT:
                shooterX_change = 5.5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('gunshot.wav')
                    bullet_sound.play()
                    bulletX = shooterX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                shooterX_change = 0

    # Boundries for spaceship
    shooterX += shooterX_change

    if shooterX <= 0:
        shooterX = 0
    elif shooterX >= 736:
        shooterX = 736

    # Boundries for aliens
    for j in range(num_of_alien):

        #Game Over
        if alienY[j] > 420:
            for i in range(num_of_alien):
                alienY[i] = 2000
            game_over_text()
            break

        alienX[j] += alienX_change[j]
        if alienX[j] <= 0:
            alienX_change[j] = 4
            alienY[j] += alienY_change[j]
        elif alienX[j] >= 736:
            alienX_change[j] = -4
            alienY[j] += alienY_change[j]

        # Collision of alien and bullet
        collision = isCollision(alienX[j], alienY[j], bulletX, bulletY)
        if collision:
            alien_sound = mixer.Sound('aliendie.wav')
            alien_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 10

            alienX[j] = random.randint(50, 735)
            alienY[j] = random.randint(40, 170)

        alien(alienX[j], alienY[j], j)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    show_score(textX,textY)
    shooter(shooterX, shooterY)
    pygame.display.update()
