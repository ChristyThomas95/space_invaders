import math
import random

import pygame
from pygame import mixer

pygame.init()
window = pygame.display.set_mode((800, 600))
background = pygame.image.load('images/background.png')
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('images/ufo.png')
pygame.display.set_icon(icon)


spaceship = pygame.image.load('images/ship.png')
playerX = 370
playerY = 480
playerX_change = 0


enemy_ship = []
enemy_x = []
enemy_y = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_ship.append(pygame.image.load('images/enemy.png'))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

laser = pygame.image.load('images/laser.png')
laser_x = 0
laser_y = 480
laser_x_change = 0
laser_y_change = 10
laser_state = "ready"

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 25)

textX = 10
testY = 10

over_font = pygame.font.Font('freesansbold.ttf', 70)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    window.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    window.blit(over_text, (200, 250))


def user_ship(x, y):
    window.blit(spaceship, (x, y))


def aliens(x, y, i):
    window.blit(enemy_ship[i], (x, y))


def laser_shot(x, y):
    global laser_state
    laser_state = "fire"
    window.blit(laser, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False
running = True
while running:
    window.fill((0, 0, 0))
    window.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if laser_state is "ready":
                    bulletSound = mixer.Sound("images/laser.wav")
                    bulletSound.play()

                    laser_x = playerX
                    laser_shot(laser_x, laser_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    for i in range(num_of_enemies):
        if enemy_y[i] > 440:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000
            game_over_text()
            break
        enemy_x[i] += enemyX_change[i]
        if enemy_x[i] <= 0:
            enemyX_change[i] = 4
            enemy_y[i] += enemyY_change[i]
        elif enemy_x[i] >= 736:
            enemyX_change[i] = -4
            enemy_y[i] += enemyY_change[i]
        collision = isCollision(enemy_x[i], enemy_y[i], laser_x, laser_y)
        if collision:
            explosionSound = mixer.Sound("images/explosion.wav")
            explosionSound.play()
            laser_y = 480
            laser_state = "ready"
            score_value += 1
            enemy_x[i] = random.randint(0, 736)
            enemy_y[i] = random.randint(50, 150)

        aliens(enemy_x[i], enemy_y[i], i)
    if laser_y <= 0:
        laser_y = 480
        laser_state = "ready"

    if laser_state is "fire":
        laser_shot(laser_x, laser_y)
        laser_y -= laser_y_change

    user_ship(playerX, playerY)
    show_score(textX, testY)
    pygame.display.update()

background = pygame.image.load('images/background.png')

