# Imports
import pygame
import random
from pygame import mixer
import time


# Initialization
pygame.init()

# Shortcuts
font = pygame.font.Font('freesansbold.ttf', 27)

#----------------------------------------------------------

# Background music
music = mixer.Sound('music.mp3')
music.set_volume(0.15)
music.play(-1)

#----------------------------------------------------------

# Generating the screen
screen = pygame.display.set_mode((700, 400))

#----------------------------------------------------------

# Sprites

# Creating a function to define the sprites
def generate(x, y, entity):
    screen.blit(entity, (x, y))

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Title Screen
titleScreenImg = pygame.image.load('TitleScreen.png')

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Score Text
score = 0
textX = 10
textY = 10

# Defining the text
def show_score(x, y):
    # Rendering the text
    scoreText = font.render("Score: " + str(score), True, (0, 0, 0))
    # Drawing the text
    screen.blit(scoreText, (x, y))

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Game Over Text
text2X = 260
text2Y = 150

# Defining the text
def gameOver(x, y):
    # Rendering the text
    overText = font.render("GAME OVER", True, (0, 0, 0))
    # Drawing the text
    screen.blit(overText, (x, y))


#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Background
bgImg = pygame.image.load('bg.png')

# Player
# Sprite is 50 wide by 107 tall
playerImg = pygame.image.load('player.png')
playerDeadImg = pygame.image.load('playerDead.png')
playerRect = playerImg.get_rect()
playerX = 50
playerY = 260
dead = False
# Jumping stuff
jump = False
# Variables for math
# Force
v = 15
# Mass
m = 0.2

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Hole
#Sprite is 72x40 pixels
holeImg = pygame.image.load('hole.png')
holeRect = holeImg.get_rect()
global holeX
holeX = random.randint(200, 1200)
holeY = 360
holeX_change = 0
holeX_rate = 10

# Making hole move
def moveHole(n):
        global holeX
        if holeX > -100:
            holeX -= n
        if holeX <= -100:
            randNum2 = random.randint(1, 40)
            if randNum2 == 10:
                holeX = 800

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Wall
# sprite is 17x52 pixels
wallImg = pygame.image.load('wall.png')
wallRect = wallImg.get_rect()
global wallX
wallX = holeX + random.randint(500, 800)
wallY = 308
wallX_change = 0
wallX_rate = 10

# Making wall move
def moveWall(n):
    global wallX
    if wallX >= -30:
        wallX -= n
    if wallX <= -30:
        randNum = random.randint(1, 40)
        if randNum == 23:
            wallX = 800

#----------------------------------------------------------

# Setting caption and icon

# Icon
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Window Caption
pygame.display.set_caption("Jumpy Game")

#----------------------------------------------------------

# Main Game Loop
running = False
var = True
run = True
increase = False
ended = False
while run:
    # Title Screen
    if running == False:
        screen.blit(titleScreenImg, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                titleScreenImg = bgImg
                running = True
    if event.type == pygame.QUIT:
        run = False
        running = False
    while running:
        # Detecting Inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                run = False
            if event.type == pygame.KEYDOWN:
                # Jumping
                if jump == False and event.key == pygame.K_UP and var == True:
                    jump = True
                    step = mixer.Sound('step.mp3')
                    step.set_volume(0.5)
                    step.play()
                if event.key == pygame.K_RIGHT and var == True:
                    increase = True
                    holeX_change = holeX_rate
                    wallX_change = wallX_rate
            if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
                increase = False
                holeX_change = 0
                wallX_change = 0

        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -            

        # Jumping

        # Code "borrowed" from https://www.geeksforgeeks.org/python-making-an-object-jump-in-pygame/
        if jump:
            # calculate force (F). F = 1 / 2 * mass * velocity ^ 2.
            F =(1 / 2)*m*(v**2)
            playerY-= F
            # decreasing velocity while going up and become negative while coming down
            v = v-1
            # object reached its maximum height
            if v<0:
                # negative sign is added to counter negative velocity
                m =-0.2
            # objected reaches its original state
            if v == -16:
                land = mixer.Sound('land.mp3')
                land.set_volume(0.5)
                land.play()
                # making isjump equal to false 
                jump = False
                # setting original values to v and m
                v = 15
                m = 0.2

        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
        # Coloring in the screen
        screen.fill((255, 255, 255))

        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
        # Increasing score
        if increase == True and var == True:
            holeX_change = holeX_rate
            wallX_change = wallX_rate
            score += 1
            wallX_rate += 0.005
            holeX_rate += 0.005

        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        # Functions
        playerRect.x = playerX
        playerRect.y = playerY
        wallRect.x = wallX
        wallRect.y = wallY
        holeRect.y = holeY
        holeRect.x = holeX
        background = screen.blit(titleScreenImg, (0, 0))
        show_score(textX, textY)
        generate(wallX, wallY, wallImg)
        generate(holeX, holeY, holeImg)
        generate(playerX, playerY, playerImg)
        moveWall(wallX_change)
        moveHole(holeX_change)

        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        # Collision
        if playerRect.colliderect(wallRect) or playerRect.colliderect(holeRect) and var == True:
            dead = True
            var = False
        if dead == True:
            gameOver(text2X, text2Y)
            if playerRect.colliderect(wallRect) and ended == False:
                ended = True
                increase = False
                holeX_change = 0
                holeX_rate = 0
                wallX_change = 0
                wallX_rate = 0
                playerImg = playerDeadImg
                music.set_volume(0)
                if playerRect.colliderect(wallRect):
                    slap = mixer.Sound('slap.wav')
                    slap.set_volume(0.5)
                    slap.play()
                break
            if playerRect.colliderect(holeRect) and ended == False:
                ended = True
                music.set_volume(0)
                increase = False
                holeX_change = 0
                holeX_rate = 0
                wallX_change = 0
                wallX_rate = 0
                for counter in range(10):
                    playerY += 20
                    background = screen.blit(titleScreenImg, (0, 0))
                    generate(wallX, wallY, wallImg)
                    generate(holeX, holeY, holeImg)
                    generate(playerX, playerY, playerImg)
                    show_score(textX, textY)
                    gameOver(text2X, text2Y)
                    pygame.display.update()
                    pygame.time.delay(20)
                slap = mixer.Sound('slap.wav')
                slap.set_volume(0.5)
                slap.play()
                break

        #-----------------------------------------------------------

        # Updating Stuff
        pygame.time.delay(20)
        pygame.display.update()
    pygame.display.update()
