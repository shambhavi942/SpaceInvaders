import pygame
import random
import math
from pygame import mixer

pygame.init()
clock = pygame.time.Clock()

# creating the game screen
screen = pygame.display.set_mode((800, 600))

# BACKGROUND
background = pygame.image.load('bbgg.jpg')

# BACKGROUND SOUND
mixer.music.load('background.mp3')
mixer.music.play(-1)

# the screen title and the icon

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('download.jpg')
pygame.display.set_icon(icon)

# Player
playerImage = pygame.image.load('ship.png')
playerX = 360
playerY = 480
playerX_change = 0

# enemy
enemyImage = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImage.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(6)
    enemyY_change.append(40)

# bullet
# ready-> you cannot see the bullet on the screen  fire->bullet is currently moving
# spacebar pressed -> bullet fired
bulletImage = pygame.image.load('bullets.png')
bulletX = 0
bulletY = 480
bulletX_change = 10
bulletY_change = 20
bullet_state = "ready"

# SCORE
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# GAME OVER TEXT
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("SCORE:" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text(x, y):
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImage, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImage[i], (x, y))


# bullet state

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImage, (x + 20, y + 15))


# collision
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# The game loop : the game screen will only be closed when the closed button is pressed and not by itself.

running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():  # event is the variable and we are looping through all the events in pygame
        if event.type == pygame.QUIT:
            running = False  # when the closed button is pressed the game will be closed.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -6
            if event.key == pygame.K_RIGHT:
                playerX_change = 6
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_Sound = mixer.Sound('shoot.wav')
                    bullet_Sound.play()
                    # get the current x cord of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    # creating boundary

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(num_of_enemies):
        # game over
        if enemyY[i] > 200:
            for j in range(num_of_enemies):
                enemyY[i] = 2000
            game_over_text(200, 250)
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 6
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -6
            enemyY[i] += enemyY_change[i]

        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('invaderkilled.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_stat = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)  # we want the player to be always seen on the screen so we add it to the while loop.
    show_score(textX, textY)
    pygame.display.update()
