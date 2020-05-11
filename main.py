import math
import random
import pygame
from pygame import mixer

# Initialize the game
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Background music
mixer.music.load('rebel-theme.wav')
mixer.music.play(-2)
mixer.music.set_volume(0.2)

# Title and Icon
pygame.display.set_caption("Star Wars")
icon = pygame.image.load('space-station.png')
pygame.display.set_icon(icon)

# Score
global score_value
score_value = 0
font = pygame.font.Font('SF Distant Galaxy AltOutline Italic.ttf', 32)

textX = 10
textY = 10

# Player
playerImg = pygame.image.load('battleship.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImgs = [pygame.image.load('aircraft.png'), pygame.image.load('spaceship_.png'),
             pygame.image.load('space-station_.png')]
current_enemyImg = enemyImgs[0]
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyX.append(random.randint(10, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(40)

# Bullet
# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 2
bulletY_change = 10
bullet_state = "ready"

# Game Over text
over_font = pygame.font.Font('SF Distant Galaxy AltOutline Italic.ttf', 64)

# Speed
enemy_speed = 3
player_speed = 4


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
    mixer.music.stop()
    game_over_music = mixer.Sound('imperial_march.wav')
    game_over_music.play()
    game_over_music.set_volume(0.1)


def player_win():
    player_win_text = over_font.render('YOU WIN', True, (255, 255, 255))
    screen.blit(player_win_text, (250, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y):
    screen.blit(current_enemyImg, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # RGB
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                playerX_change = -player_speed
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                playerX_change = player_speed
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('blaster-firing.wav')
                    bullet_sound.play()
                    bullet_sound.set_volume(0.2)
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                playerX_change = 0

    # Player movement
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 450:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        if score_value >= 30:
            player_win()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = enemy_speed
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -enemy_speed
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            explosion_sound.set_volume(0.1)
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(10, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i])

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    if score_value >= 5:
        enemy_speed = 4
    if score_value >= 10:
        enemy_speed = 6
        player_speed = 8
    if score_value >= 15:
        num_of_enemies = 3
        enemy_speed = 7
        current_enemyImg = enemyImgs[1]
    if score_value >= 25:
        num_of_enemies = 1
        enemy_speed = 8
        current_enemyImg = enemyImgs[2]

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
