import pygame
import random
import math
pygame.init()

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Space Wars")
icon = pygame.image.load('img/logo1.png')
pygame.display.set_icon(icon)

bgImage = pygame.image.load('img/bg.png')

# score
score = 0
font = pygame.font.Font('freesansbold.ttf', 25)
textX = 5
textY = 5

# gameover
over = pygame.font.Font('freesansbold.ttf', 64)


def game_Over():
    over_text = over.render("GAME OVER", True, (128, 128, 128))
    screen.blit(over_text, (200, 250))


def show_Score(x, y):
    score1 = font.render("Score: " + str(score), True, (128, 128, 128))
    screen.blit(score1, (x, y))


# explosion
expImg = pygame.image.load('img/explosion.png')


def explode(x, y):
    screen.blit(expImg, (x, y))

# collision


def collide(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX, 2)) +
                         (math.pow(enemyY-bulletY, 2)))
    if distance < 28:
        return True
    else:
        return False


# bullet
bulletImg = pygame.image.load('img/bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = 1
bullet_state = "ready"


def fire(x, y):
    screen.blit(bulletImg, (x, y))


# player
playerImg = pygame.image.load('img/player.png')
playerX = 370
playerY = 480
playerX_change = 0


def player(x, y):
    screen.blit(playerImg, (x, y))


# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('img/enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(0, 50))
    enemyY_change.append(0.1)


def enemy(x, y, i):
    screen.blit(enemyImg[i], (enemyX[i], enemyY[i]))


running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(bgImage, (0, 0))
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                playerX_change = -0.7
            elif event.key == pygame.K_d:
                playerX_change = 0.7
            elif event.key == pygame.K_SPACE:
                bullet_state = "fire"

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                playerX_change = 0

    # enemy movement
    for i in range(num_of_enemies):
        if enemyY[i] >= 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_Over()
            break
        enemyY[i] += enemyY_change[i]

        collision = collide(enemyY[i], enemyX[i], bulletY, bulletX)

        if collision:
            score += 1
            bullet_state = "ready"
            bulletY = 480
            enemyImg[i] = pygame.image.load('img/enemy.png')
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(0, 50)
            enemyY_change[i] = 0.1

        enemy(enemyX[i], enemyY[i], i)

    # player movement
    if playerX >= 736:
        playerX = 736
    elif playerX <= 0:
        playerX = 0

    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = 480

    if bullet_state == "ready":
        fire(bulletX+16, bulletY)
        bulletX = playerX
    elif bullet_state == "fire":
        bulletY -= bulletY_change
        fire(bulletX+16, bulletY)

    show_Score(textX, textY)
    player(playerX, playerY)

    playerX += playerX_change

    pygame.display.update()
