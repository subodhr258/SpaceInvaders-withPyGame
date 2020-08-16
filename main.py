import pygame
import os
import random
import math
from pygame import mixer

#initialize the pygame:
pygame.init()

#create the screen
screen = pygame.display.set_mode((800,600)) #width,height

#Title and Icon
pygame.display.set_caption("Space Invaders")

current_path = os.path.dirname(__file__) # Where your .py file is located
resource_path = os.path.join(current_path, 'resources') # The resource folder path
image_path = os.path.join(resource_path, 'images') # The image folder path
icon = pygame.image.load(os.path.join(image_path,"ufo.png"))
pygame.display.set_icon(icon)

#background
background = pygame.image.load(os.path.join(image_path,"background.png"))

#background sound
sound_path = os.path.join(resource_path, 'sound')
mixer.music.load(os.path.join(sound_path,'background.wav'))
mixer.music.play(-1)

#Player
playerImg = pygame.image.load(os.path.join(image_path,"spaceship.png"))
playerX = 370
playerY = 480
playerX_change = 0

#enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 15
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load(os.path.join(image_path,"enemy.png")))
    enemyX.append(random.randint(0,736)) 
    enemyY.append(random.randint(50,150))
    enemyX_change.append(4)
    enemyY_change.append(40)

#bullet
bulletImg = pygame.image.load(os.path.join(image_path,"bullet.png"))
bulletX = 0
bulletY = 480
bulletY_change = 10
bullet_state = "ready"

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10

#game over Text
over_font = pygame.font.Font('freesansbold.ttf',64)

def show_score(x,y):
    score = font.render("Score :"+str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

def game_over_text():
    over_text = over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text,(200,250))

def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x+16,y+10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX,2) + math.pow(enemyY - bulletY,2))
    if distance<27:
        return True
    return False

#the game loop
running = True
while running:
    #RGB background:
    screen.fill((30,30,30))
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                playerX_change = -5
            if event.key == pygame.K_d:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state=="ready":
                    bullet_Sound = mixer.Sound(os.path.join(sound_path,'laser.wav'))
                    bullet_Sound.play()
                    bulletX=playerX
                    fire_bullet(bulletX,bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                playerX_change = 0

    playerX+=playerX_change
    
    if playerX < 0:
        playerX=0
    elif playerX > 736:
        playerX=736
    #enemy movement
    for i in range(num_of_enemies):
        #Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i]+=enemyX_change[i]
        if enemyX[i] < 0:
            enemyX[i]=0
            enemyX_change[i]=3
            enemyY[i]+=enemyY_change[i]
        elif enemyX[i] > 736:
            enemyX[i]=736
            enemyX_change[i]=-3
            enemyY[i]+=enemyY_change[i]
        #Collision
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosion_Sound = mixer.Sound(os.path.join(sound_path,'explosion.wav'))
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value+=1
            enemyX[i] = random.randint(0,736)
            enemyY[i] = random.randint(50,150)

        enemy(enemyX[i],enemyY[i],i)


    if bulletY<=0:
        bulletY=480
        bullet_state="ready"

    if bullet_state =="fire":
        fire_bullet(bulletX,bulletY)
        bulletY-=bulletY_change


    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()