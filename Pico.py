import random
import pygame
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import time
from pygame import mixer
 

pygame.init()
 

width, height = 1280, 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pico")
mixer.music.load("ROY KNOX - Lost In Sound (Magic Free Release).wav")
mixer.music.play(-1)

fps = 30
clock = pygame.time.Clock()
 

cap = cv2.VideoCapture(0)
cap.set(3, 1280)  
cap.set(4, 720)  
 

imgBalloon = pygame.image.load('BalloonRed.png').convert_alpha()
imgvic = pygame.image.load('HeroesOfTheStorm_victory1-1024x576.png').convert_alpha()
rectBalloon = imgBalloon.get_rect()
rectBalloon.x, rectBalloon.y = 500, 300
 

speed = 15
score = 0
startTime = time.time()
totalTime = 100
 

detector = HandDetector(detectionCon=0.8, maxHands=2)
 
 
def resetBalloon():
    rectBalloon.x = random.randint(100, img.shape[1] - 100)
    rectBalloon.y = img.shape[0] + 50
 
 

start = True
while start:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()
 
    
    timeRemain = int(totalTime -(time.time()-startTime))
    if timeRemain <0:
        window.fill((255,255,255))
 
        font = pygame.font.Font('Marcellus-Regular.ttf', 50)
        textScore = font.render(f'Your Score: {score}', True, (50, 50, 255))
        textTime = font.render(f'Time UP', True, (50, 50, 255))
        window.blit(textScore, (450, 350))
        window.blit(textTime, (530, 275))
 
    else:
        
        success, img = cap.read()
        img = cv2.flip(img, 1)
        hands, img = detector.findHands(img, flipType=False)
 
        rectBalloon.y -= speed  
        
        if rectBalloon.y < 0:
            resetBalloon()
            speed += 1
 
        if hands and len(hands) == 2:
            hand1, hand2 = hands[0], hands[1]
            x1, y1 = hand1['lmList'][8][0:2]  # fingertip of hand 1
            x2, y2 = hand2['lmList'][8][0:2]  # fingertip of hand 2
            if rectBalloon.collidepoint(x1, y1) or rectBalloon.collidepoint(x2, y2):
                resetBalloon()
                score += 10
                speed += 1
 
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgRGB = np.rot90(imgRGB)
        frame = pygame.surfarray.make_surface(imgRGB).convert()
        frame = pygame.transform.flip(frame, True, False)
        window.blit(frame, (0, 0))
        window.blit(imgBalloon, rectBalloon)
 
        font = pygame.font.Font('Marcellus-Regular.ttf', 50)
        textScore = font.render(f'Score: {score}', True, (50, 50, 255))
        textTime = font.render(f'Time: {timeRemain}', True, (50, 50, 255))
        window.blit(textScore, (35, 35))
        window.blit(textTime, (1000, 35))
    if score>200:
        pass
    
    pygame.display.update()
   
    clock.tick(fps)