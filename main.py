#!/usr/bin/python2

# Author : Amutha Bharathi 

import pygame
import pygame.mixer

import time
import datetime as dt
import sys
import sprite_func
import math
from random import randint


screen_w = 1920
screen_h = 1080
screen_size = (screen_w, screen_h)

screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("SHOOT THE BEAR")

#Colors
red = (255,0,0)
green = (0,255,0)
lgreen = (0,90,0)

blue = (0,0,255)
black = (0,0,0)
white = (255,255,255)
gray = (80,80,80)
dgray = (40,40,40)
lgray = (240,240,240)

#pygame.key.set_repeat(5,5)
pygame.key.set_repeat()
i = 0
x_pos = 270
y_pos = 270
orig = (x_pos,y_pos)

width = 270
height = 270


pix_step = 10
running = True
ss_hndl = sprite_func.SpriteSheet("data/images/walk-cycle-boy-hi.png")            
frame = 0
row = 0
img_1 = ss_hndl.get_image(120*frame,row*187,120,154)
sprite_pos = 0
direction = 0

bg = pygame.image.load("data/images/bg.jpg")

with_arr_top_square = pygame.image.load("data/images/with_arr_top_square.png");
with_arr_bot_symmetric = pygame.image.load("data/images/with_arr_bot_symmetric.png");
with_arr_top_relaxed_square = pygame.image.load("data/images/with_arr_top_relaxed_square.png")
bear_big =pygame.image.load("data/images/bear_final.png")
bear = pygame.transform.scale(bear_big, (100,180))
arrow = pygame.image.load("data/images/arrow.png")
blood = pygame.image.load("data/images/blood_final.png")
blood = pygame.transform.scale(blood, (120,120))
img_2 = with_arr_bot_symmetric



aim  = 0 
deg = 0
display_changed = False
time_out = True
ref_time = 0.0
now_time = 0.0
target_x = 0
target_y = 0

hit_counter = 0

pygame.init()

myfont = pygame.font.SysFont("consolas", 72)
text = myfont.render("hello world", 0, (0,0,0))

pygame.mixer.init(44100, -16,2, 2048)

pygame.mixer.music.load("data/music/funny.mp3")
pygame.mixer.music.play(-1)

screen.fill(white)
pygame.display.flip()

def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def compute_hit():
    x = 0.0
    y = 0.0
    x = float(abs(120+sprite_pos - target_x))
    y = float(abs(500 - target_y))
    
    print "x = ", x, " y = ", y

    compute_deg = math.degrees(math.atan(y/x)) # compute the bear's angle wrt hunter
    
    print "compute_deg = ", compute_deg, " deg = ", deg
    
    if abs(compute_deg-deg) < 8:
        return True
    else:
        return False


while running:
    if time_out == True:
        pygame.draw.rect(screen, white, (target_x, target_y, 180, 180),0)
        ref_time = dt.datetime.now()
        time_out = False
        target_x = randint(800,1800)
        target_y = randint(40,380)
        screen.blit(bear,(target_x, target_y))
        pygame.display.flip()
        
    now_time = dt.datetime.now()
    
    if (now_time-ref_time).seconds > 5:
        
        time_out = True


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP and aim == 1:
                display_changed = True
                if direction == 0: #facing left
                    deg += 2
                    deg = 90 if deg>90 else deg
                    img_1 = rot_center(with_arr_top_square,deg)
                else:
                    deg -= 2
                    deg = 0 if deg<0 else deg
                    img_1 = pygame.transform.flip(with_arr_top_square, True, False)
                    img_1 = rot_center(img_1,deg)
                
            if event.key == pygame.K_DOWN and aim == 1:
                display_changed = True
                if direction == 0: #facing left
                    deg -= 2
                    deg = 0 if deg<0 else deg
                    img_1 = rot_center(with_arr_top_square,deg)
                else:
                    deg += 2
                    deg = 90 if deg>90 else deg
                    img_1 = pygame.transform.flip(with_arr_top_square, True, False)
                    img_1 = rot_center(img_1,deg)

            if event.key == pygame.K_LEFT and aim == 0:
              #print "You pressed LEFT"
                display_changed = True
                direction = 0 #left
                frame += 1
                if frame == 4:
                    frame = 0
                    row ^= 1 
                sprite_pos -= 15

                img_1 = ss_hndl.get_image(120*frame,row*187,120,154)
                
            if event.key == pygame.K_RIGHT and aim == 0:
              #print "You pressed RIGHT"
                display_changed = True
                direction = 1 #right
                frame += 1
                if frame == 4:
                    frame = 0
                    row ^= 1 
                sprite_pos += 15
                img_1 = ss_hndl.get_image(120*frame,row*187,120,154)
                img_1 = pygame.transform.flip(img_1, True, False)

            if event.key == pygame.K_SPACE:
                
                display_changed = True
                aim ^= 1
                deg = 0
                if aim == 1:
                    if direction == 0: # facing left
                        img_1 = with_arr_top_square
                        img_2 = with_arr_bot_symmetric

                    elif direction == 1:
                        img_1 = pygame.transform.flip(with_arr_top_square, True, False)
                        img_2 = pygame.transform.flip(with_arr_bot_symmetric, True, False)
                elif aim == 0:
                    if direction == 0:
                        img_1 = ss_hndl.get_image(120*frame,row*187,120,154) 
                    elif direction == 1:
                        img_1 = ss_hndl.get_image(120*frame,row*187,120,154)
                        img_1 = pygame.transform.flip(img_1, True, False)


            if event.key == pygame.K_RETURN:
                #deg = 0
                aim = 1
                display_changed = True
                
                if direction == 0:
                    img_1 = rot_center(with_arr_top_relaxed_square,deg)
                    img_2 = with_arr_bot_symmetric
                else:
                    img_1 = pygame.transform.flip(with_arr_top_relaxed_square,True,False)
                    img_1 = rot_center(img_1,deg)
                    
                    img_2 = pygame.transform.flip(with_arr_bot_symmetric, True, False)
                
                if compute_hit() == True:
                    print "Hit"
                    hit_counter += 1
                    m = math.tan(math.radians(deg)) # slope
                    c = 500 - m*(sprite_pos+120)  # c = y - mx //line equation
#compute new y position
                    i = 0
                    pygame.draw.rect(screen, white, (120+sprite_pos, 480, 200, 100),0)
                    screen.blit(img_1,(120+sprite_pos,480))
                    screen.blit(img_2,(120+sprite_pos+5,500+98)) #top image height is 101 so shift bottom
                   
#For x values in the following range compute y and render arrow animation
                    for i in range(sprite_pos+330,target_x-120, 50):
                        arrow_y = m*i + c
                        rot_arrow = rot_center(arrow, deg)

                        screen.blit(rot_arrow,(i, 1000-arrow_y))
                        pygame.display.flip()
                        time.sleep(0.01)

                        pygame.draw.rect(screen, white, (i, 1005-arrow_y, 100, 100),0)
                        pygame.display.flip()
                        time.sleep(0.01)

                    screen.blit(blood,(target_x,target_y))
                    pygame.display.flip()
                    time.sleep(1)

                else:
                    print "Missed"
                    m = math.tan(math.radians(deg)) # slope
                    c = 500 - m*(sprite_pos+120)  # c = y - mx //line equation
#compute new y position
                    i = 0
                    pygame.draw.rect(screen, white, (120+sprite_pos, 480, 200, 100),0)
                    screen.blit(img_1,(120+sprite_pos,480))
                    screen.blit(img_2,(120+sprite_pos+5,500+98)) #top image height is 101 so shift bottom
                   
#For x values in the following range compute y and render arrow animation
                    for i in range(sprite_pos+330,1920, 50):
                        arrow_y = m*i + c
                        rot_arrow = rot_center(arrow, deg)

                        screen.blit(rot_arrow,(i, 1000-arrow_y))
                        pygame.display.flip()
                        time.sleep(0.01)

                        pygame.draw.rect(screen, white, (i, 1005-arrow_y, 100, 100),0)
                        pygame.display.flip()
                        time.sleep(0.01)

                    pygame.display.flip()
                    time.sleep(1)
            
            if display_changed == True:
                screen.fill(white)
                if aim == 1:
                    screen.blit(img_1,(120+sprite_pos,480))
                    screen.blit(img_2,(120+sprite_pos+5,500+98)) #top image height is 101 so shift bottom
                else:
                    screen.blit(img_1,(120+sprite_pos,500))
                screen.blit(bear,(target_x, target_y))    
                str2 = str(hit_counter)
                hit_val = "Hits : "+str2
                text = myfont.render(hit_val, 0, (0,0,0))
                screen.blit(text, (800,970))
                pygame.draw.line(screen,black,(0,654),(1920,654), 10)
                
                pygame.display.flip()
                display_changed = False

            pygame.event.clear()

            time.sleep(0.07)

