import cv2 as cv
import numpy as np
import pygame

surface = pygame.display.set_mode((1392,459))

rect = pygame.Rect(290, 0, 390, 162)
sub = screen.subsurface(rect)

pygame.image.save(sub, "screenshot.jpg")
time.sleep(0.01)
downlane = cv.imread('screenshot.jpg')

img_gray = cv.cvtColor(downlane, cv.COLOR_BGR2GRAY)

template = cv.imread('images/down/bike.png',0)

w, h = template.shape[::-1]
res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)
threshold = 0.5
loc = np.where( res >= threshold)
print(loc)
i = 0
r = 5
real_locs = []
prev_x , prev_y = 0,0
for l in range(len(loc[0])):
    x = loc[0][l]
    y = loc[1][l]
    if (x-prev_x) <=r and (y-prev_y)<=r:
        continue
    else:
        real_locs.append([x,y])
        prev_x = x
        prev_y = y
    print(real_locs)
        
color = (255,0,0)
for ps in real_locs:
    pygame.draw.rect(surface, color, pygame.Rect(290+ps[0], ps[1],290+ps[0]+w, ps[1]+h),  2)
