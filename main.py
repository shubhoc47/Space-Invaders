import pygame
import random
import math
from pygame import mixer

pygame.init()  # Initilizing the pygame
screen = pygame.display.set_mode((800, 600))
bulletStatus = False
font = pygame.font.Font('fjallaOne-Regular.ttf', 33)
over = pygame.font.Font('fjallaOne-Regular.ttf', 90)

mixer.music.load("background.wav")
mixer.music.play(-1)

def show_score(score):
    point = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(point, (9, 9))

def gameover():
    point = over.render("GAME OVER", True, (255, 255, 255))
    screen.blit(point, (200, 250))

def bulletFire(image, X, Y):
    global bulletStatus
    bulletStatus = True
    screen.blit(image, (X + 16, Y + 10))


def IsCollusion(EnemyX, EnemyY, BulletX, BulletY):
    distance = math.sqrt(math.pow((BulletX - EnemyX), 2) + math.pow((BulletY - EnemyY), 2))
    return distance <= 27


def player(image, X, Y):
    if X >= 736:
        X = 736
    elif X < 0:
        X = 0
    if Y >= 480:
        Y = 480
    elif Y < 0:
        Y = 0
    screen.blit(image, (X, Y))


def enemy(image, X, Y, Number):
    for i in range(Number):
        screen.blit(image[i], (X[i], Y[i]))


if __name__ == '__main__':
    # Creating screen for game
    # screen = pygame.display.set_mode((800, 600))

    pygame.display.set_caption("Sky Invaders")
    icon = pygame.image.load("spaceship2.jpg")
    pygame.display.set_icon(icon)
    playerImg = pygame.image.load("space-invaders.png")
    background = pygame.image.load("space.jpg")
    BulletImg = pygame.image.load("rsz_bullet.png")
    playerX = 370
    playerY = 480
    PlayerChangeX = 0
    PlayerChangeY = 0

    EnemyImg = []
    EnemyX = []
    EnemyY = []
    EnemyChangeX = []
    EnemyChangeY = []
    EnemyNumber = 6

    for i in range(6):
        EnemyImg.append(pygame.image.load("alien-2.png"))
        EnemyX.append(random.randint(0, 736))
        EnemyY.append(random.randint(30, 150))
        EnemyChangeX.append(2)
        EnemyChangeY.append(0)

    BulletX = 0
    BulletY = 480
    BulletChangeX = 0
    BulletChangeY = 6
    point = 0
    flag = True

    while flag:
        # To Change background colour
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    PlayerChangeX = -1
                elif event.key == pygame.K_RIGHT:
                    PlayerChangeX = 1
                if event.key == pygame.K_UP:
                    PlayerChangeY = -1
                elif event.key == pygame.K_DOWN:
                    PlayerChangeY = 1
                if event.key == pygame.K_SPACE:
                    # print(bulletStatus)
                    if not bulletStatus:
                        BulletSound = mixer.Sound("laser.wav")
                        BulletSound.play()
                        BulletX = playerX
                        BulletY = playerY
                        bulletFire(BulletImg, playerX, BulletY)
                        # print(k)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    PlayerChangeX = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    PlayerChangeY = 0

        for i in range(EnemyNumber):
            EnemyX[i] += EnemyChangeX[i]
            EnemyY[i] += EnemyChangeY[i]
            if EnemyX[i] >= 736:
                EnemyChangeX[i] = -0.5
                EnemyY[i] += 30

            elif EnemyX[i] < 0:
                EnemyChangeX[i] = 0.5
                EnemyY[i] += 30


        playerX += PlayerChangeX
        playerY += PlayerChangeY

        if playerX < 0:
            playerX = 0
        if playerX > 736:
            playerX = 736

        if playerY < 0:
            playerY = 0
        if playerY > 480:
            playerY = 480


        if BulletY <= 0:
            BulletY = playerY
            bulletStatus = False
        if bulletStatus:
            bulletFire(BulletImg, BulletX, BulletY)
            BulletY -= BulletChangeY
            # print(k)
        for i in range(EnemyNumber):
            collusion = IsCollusion(EnemyX[i], EnemyY[i], BulletX, BulletY)
            if collusion:
                CollusionSound = mixer.Sound("explosion.wav")
                CollusionSound.play()
                if bulletStatus:
                    point += 1
                    # print(point)
                BulletY = playerY
                bulletStatus = False
                EnemyX[i] = random.randint(0, 736)
                EnemyY[i] = random.randint(30, 150)

            playerCollusion = IsCollusion(EnemyX[i], EnemyY[i], playerX, playerY)

            if EnemyY[i] >= 480 or playerCollusion:
                gameover()
                for i in range(EnemyNumber):
                    EnemyY[i] = 999

        player(playerImg, playerX, playerY)
        enemy(EnemyImg, EnemyX, EnemyY, EnemyNumber)
        show_score(point)
        pygame.display.update()
