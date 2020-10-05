import pygame
import random
import math
from pygame import mixer
import time

# initialise pygame
pygame.init()
# creates screen, width, height
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption("Unicorn Fighters")
icon = pygame.image.load("unicorn.png")
pygame.display.set_icon(icon)

# Background
background = pygame.image.load('background.png')

# Background Sounds
mixer.music.load('background.mp3')
mixer.music.play(-1) #plays on loop

# Player
playerImg = pygame.image.load("char.png")
playerX = 370  # we are including the 30 pixels
playerY = 480
playerX_change = 0

# Bomb
num_of_bombs = 2
bombImg = []
bombX = []
bombY = []
bombX_change = []
bombY_change = []
for k in range(num_of_bombs):
    bombImg.append(pygame.image.load('bomb.png'))
    bombX.append(random.randint(2, 760))  # we are including the 30 pixels
    bombY.append(random.randint(50, 150))
    bombX_change.append(1.3)
    bombY_change.append(40)

# Aliens/Enemies List, we then store each enemy inside
num_of_enemies = 5
alienImg = []
alienX = []
alienY = []
alienX_change = []
alienY_change = []
#appending each of the 5 enemies into the list
for i in range(num_of_enemies):
    alienImg.append(pygame.image.load("monster.png"))
    alienX.append(random.randint(2, 760))  # we are including the 30 pixels
    alienY.append(random.randint(50, 150))
    alienX_change.append(0.1)
    alienY_change.append(40)

# Bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletX_change = 0
bulletY = 480
bulletY_change = 1.5
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',25)
scoreX = 10
scoreY = 10

#Gameover
game_over_font = pygame.font.Font('freesansbold.ttf', 64)

# defining classes to put into the infinite loop

def show_score(x,y):
    score = font.render('Score: ' + str(score_value), True, (255,255,255))
    screen.blit(score, (x,y))

def game_over_text():
    game_over = game_over_font.render('GAME OVER', True, (255,255,255))
    screen.blit(game_over, (200,250))

def player(x, y):
    screen.blit(playerImg, (x, y))  # to draw it on the screen


def alien(x, y, i):
    screen.blit(alienImg[i], (x, y))

def bomb(x, y, k):
    screen.blit(bombImg[k], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(alienX, alienY, bulletX, bulletY):
    distance = math.sqrt(math.pow(alienX - bulletX, 2) + math.pow(alienY - bulletY, 2))
    if distance < 30:
        return True
    else:
        return False

def isBombed(bombX, bombY, bulletX, bulletY):
    distance2 = math.sqrt(math.pow(bombX - bulletX, 2) + math.pow(bombY - bulletY, 2))
    if distance2 < 15:
        return True
    else:
        return False

# infinite loop of events
# if there is an event of clicking close, == quit.
running = True

while running:

    screen.fill((149, 144, 182))  # rgb
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:  # meaning key is pressed down
            print("a keystroke is pressed")
            if event.key == pygame.K_LEFT:
                playerX_change = -1
                print("left arrow is pressed")
            if event.key == pygame.K_RIGHT:
                playerX_change = 1
                print("right arrow is pressed")
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    shoot_sound = mixer.Sound('shoot.wav')
                    shoot_sound.play()

                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
                print("keystroke has been released")

    # Player boundary
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):
        # Game Over
        if alienY[i] > 400:
            for j in range(num_of_enemies):
                alienY[j] = 2000
            game_over_text()
            break

        alienX[i] += alienX_change[i]

        if alienX[i] <= 0:
            alienX_change[i] = 0.6
            alienY[i] += alienY_change[i]
        elif alienX[i] >= 736:
            alienX_change[i] = -0.6
            alienY[i] += alienY_change[i]

        # Collision
        collision = isCollision(alienX[i], alienY[i], bulletX, bulletY)
        if collision:
            hit_sound = mixer.Sound('hit.wav')
            hit_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            print(score_value)
            alienX[i] = random.randint(30, 760)
            alienY[i] = random.randint(50, 150)

        alien(alienX[i], alienY[i], i)

        #Bomb Collision
    for k in range(num_of_bombs):
        if bombY[k] > 400:
            bombX[k] = random.randint(30, 760)
            bombY[k] = random.randint(50, 150)
            
        collisionbomb = isBombed(bombX[k], bombY[k], bulletX, bulletY)
        if collisionbomb:
            hit_sound = mixer.Sound('hit.wav')
            hit_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value -= 1
            bombX[k] = random.randint(30, 760)
            bombY[k] = random.randint(50, 150)


        bomb(bombX[k], bombY[k], k)

          #bomb movement
        bombX[k] += bombX_change[k]

        if bombX[k] <= 0:
            bombX_change[k] = 1.0
            bombY[k] += bombY_change[k]
        elif bombX[k] >= 736:
            bombX_change[k] = -1.0
            bombY[k] += bombY_change[k]

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 400
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)  # indicating the x and y coordinates
    show_score(scoreX, scoreY)
    pygame.display.update()
