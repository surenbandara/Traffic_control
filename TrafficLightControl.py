import random
import time
import threading
import pygame
import sys
import os
import cv2 as cv
import numpy as np
import numpy as np

vehicalload = {0:0, 1:0, 2:0, 3:0}
vehicalload2 = {0:0, 1:0, 2:0, 3:0}

# Default values of signal timers
defaultGreen = {0:0, 1:0, 2:0, 3:0}
defaultRed = 150
defaultYellow = 5

signals = []
noOfSignals = 4
currentGreen = 0   # Indicates which signal is green currently
nextGreen = (currentGreen+1)%noOfSignals    # Indicates which signal will turn green next
currentYellow = 0   # Indicates whether yellow signal is on or off


defaultGreen2 = {0:0, 1:0, 2:0, 3:0}
signals2 = []
noOfSignals2 = 4
currentGreen2 = 0   # Indicates which signal is green currently
nextGreen2 = (currentGreen2+1)%noOfSignals2    # Indicates which signal will turn green next
currentYellow2 = 0   # Indicates whether yellow signal is on or off 

speeds = {'car':2.25, 'bus':1.8, 'truck':1.8, 'bike':2.5}  # average speeds of vehicles

# Coordinates of vehicles' start
x = {'right':[0,0,0], 'down':[380,361,342], 'left':[1392,1392,1392], 'up':[298,300,322], 'down2':[1094,1075,1057], 'up2':[995,1004,1031]}    
y = {'right':[170,178,195], 'down':[0,0,0], 'left':[250,235,217], 'up':[457,457,457], 'down2':[0,0,0], 'up2':[457,457,457]}

vehicles = {'right': {0:[], 1:[], 2:[], 'crossed':0},'right2': {0:[], 1:[], 2:[], 'crossed':0}, 'down': {0:[], 1:[], 2:[], 'crossed':0}, 'up': {0:[], 1:[], 2:[], 'crossed':0}, 'down2': {0:[], 1:[], 2:[], 'crossed':0},'left2': {0:[], 1:[], 2:[], 'crossed':0},'left': {0:[], 1:[], 2:[], 'crossed':0},'up2': {0:[], 1:[], 2:[], 'crossed':0}}
vehicleTypes = {0:'car', 1:'bus', 2:'truck', 3:'bike'}
directionNumbers = {0:'right', 1:'down', 2:'left', 3:'up', 4:'down2', 5:'up2'}

directionNumbers1 = {0:'right', 1:'down', 2:'left2', 3:'up'}
directionNumbers2 = {0:'right2', 1:'down2', 2:'left', 3:'up2'}

# Coordinates of signal image, timer, and vehicle count


signalCoods_1 = [(250,100),(415,100),(415,275),(250,275)]
signalTimerCoods_1 = [(250,75),(415,75),(415,325),(250,325)]

signalCoods_2 = [(970,100),(1135,100),(1135,275),(970,275)]
signalTimerCoods_2 = [(970,75),(1135,75),(1135,325),(970,325)]

# Coordinates of stop lines
stopLines = {'right': 285,'right2': 1010, 'down': 140, 'up': 275, 'down2': 150 ,'up2': 275, 'left': 1110,'left2': 410}

defaultStop = {'right': 279,'right2': 1000, 'down': 135, 'up': 282, 'down2': 145, 'up2': 282 ,'left': 1115,'left2': 420}

# Gap between vehicles
stoppingGap = 5    # stopping gap
movingGap = 5  # moving gap

# set allowed vehicle types here
allowedVehicleTypes = {'car': True, 'bus': True, 'truck': True, 'bike': True}
allowedVehicleTypesList = []
vehiclesTurned = {'right': {1:[], 2:[]},'right2': {1:[], 2:[]}, 'down': {1:[], 2:[]}, 'up': {1:[], 2:[]},'down2': {1:[], 2:[]},'up2': {1:[], 2:[]}, 'left': {1:[], 2:[]},'left2': {1:[], 2:[]}}
vehiclesNotTurned = {'right': {1:[], 2:[]}, 'right2': {1:[], 2:[]},'down': {1:[], 2:[]}, 'up': {1:[], 2:[]},'down2': {1:[], 2:[]},'up2': {1:[], 2:[]}, 'left': {1:[], 2:[]},'left2': {1:[], 2:[]}}
rotationAngle = 3
# mid = {'right': {'x':705, 'y':445}, 'down': {'x':695, 'y':450}, 'left': {'x':695, 'y':425}, 'up': {'x':695, 'y':400}}
mid = {'right': {'x':320, 'y':215},'right2': {'x':1040, 'y':220}, 'down': {'x':350, 'y':200}, 'up': {'x':350, 'y':230},'down2': {'x':1060, 'y':207},'left': {'x':1070, 'y':220},'left2': {'x':380, 'y':220},'up2': {'x':1060, 'y':230}}


timeElapsed = 0
simulationTime = 1500
timeElapsedCoods = (600,50)
vehicleCountTexts = ["0", "0", "0", "0"]
vehicleCountCoods = [(250,50),(415,50),(415,375),(250,375)]

vehicleCountTexts2 = ["0", "0", "0", "0"]
vehicleCountCoods2 = [(970,50),(1135,50),(1135,375),(970,375)]

pygame.init()
simulation = pygame.sprite.Group()

class TrafficSignal:
    def __init__(self, red, yellow, green):
        self.red = red
        self.yellow = yellow
        self.green = green
        self.signalText = ""
        
class Vehicle(pygame.sprite.Sprite):
    def __init__(self, lane, vehicleClass, direction_number, direction, will_turn):
        pygame.sprite.Sprite.__init__(self)
        self.lane = lane
        self.vehicleClass = vehicleClass
        self.speed = speeds[vehicleClass]
        self.direction_number = direction_number
        self.direction = direction

        self.x = x[direction][lane]
        self.y = y[direction][lane]
        self.crossed = 0
        self.crossed2 = 0
        self.willTurn = will_turn[0]
        self.willTurn2 = will_turn[1]
        self.turned = 0
        self.turned2 = 0
        self.pathchanged=0
        
        self.midroad = 0
        self.rotateAngle = 0
        self.rotateAngle2 = 0

     
        
        vehicles[direction][lane].append(self)
        self.index = len(vehicles[direction][lane]) - 1
        self.crossedIndex = 0
        self.crossedIndex2 = 0
        
        path = "images/" + direction + "/" + vehicleClass + ".png"
        self.originalImage = pygame.image.load(path)
        self.image = pygame.image.load(path)
        

        self.templeft2=  self.image.get_rect().width + stoppingGap
           # x[direction][lane] += self.templeft2

        if(len(vehicles[direction][lane])>1 and vehicles[direction][lane][self.index-1].crossed==0):
            
            if(direction=='right'):
                self.stop = vehicles[direction][lane][self.index-1].stop 
                - vehicles[direction][lane][self.index-1].image.get_rect().width 
                - stoppingGap         
            elif(direction=='left'):
                self.stop = vehicles[direction][lane][self.index-1].stop 
                + vehicles[direction][lane][self.index-1].image.get_rect().width 
                + stoppingGap
            elif(direction=='down'):
                self.stop = vehicles[direction][lane][self.index-1].stop 
                - vehicles[direction][lane][self.index-1].image.get_rect().height 
                - stoppingGap
            elif(direction=='up'):
                self.stop = vehicles[direction][lane][self.index-1].stop 
                + vehicles[direction][lane][self.index-1].image.get_rect().height 
                + stoppingGap
            elif(direction=='down2'):
                self.stop = vehicles[direction][lane][self.index-1].stop 
                - vehicles[direction][lane][self.index-1].image.get_rect().height 
                - stoppingGap
            elif(direction=='up2'):
                self.stop = vehicles[direction][lane][self.index-1].stop 
                + vehicles[direction][lane][self.index-1].image.get_rect().height 
                + stoppingGap
            elif(direction=='right2'):
                self.stop = vehicles[direction][lane][self.index-1].stop 
                - vehicles[direction][lane][self.index-1].image.get_rect().width 
                - stoppingGap         
            elif(direction=='left2'):
                self.stop = vehicles[direction][lane][self.index-1].stop 
                + vehicles[direction][lane][self.index-1].image.get_rect().width 
                + stoppingGap
        else:
            self.stop = defaultStop[direction]
            
            
        # Set new starting and stopping coordinate
        if(direction=='right'):
            temp = self.image.get_rect().width + stoppingGap    
            x[direction][lane] -= temp
        elif(direction=='left'):
            temp = self.image.get_rect().width + stoppingGap
            x[direction][lane] += temp
        elif(direction=='right2'):
            temp = self.image.get_rect().width + stoppingGap    
            x[direction][lane] -= temp
        elif(direction=='left2'):
            temp = self.image.get_rect().width + stoppingGap
            x[direction][lane] += temp
        elif(direction=='down'):
            temp = self.image.get_rect().height + stoppingGap
            y[direction][lane] -= temp
        elif(direction=='up'):
            temp = self.image.get_rect().height + stoppingGap
            y[direction][lane] += temp
        elif(direction=='down2'):
            temp = self.image.get_rect().height + stoppingGap
            y[direction][lane] -= temp
        elif(direction=='up2'):
            temp = self.image.get_rect().height + stoppingGap
            y[direction][lane] += temp
        simulation.add(self)

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self):

        if(self.direction=='right'):
            if(self.crossed==0 and self.x+self.image.get_rect().width>stopLines[self.direction]):
                self.crossed = 1
                vehicles[self.direction]['crossed'] += 1
                if(self.willTurn==0):
                    vehiclesNotTurned[self.direction][self.lane].append(self)
                    self.crossedIndex = len(vehiclesNotTurned[self.direction][self.lane]) - 1

                    self.direction="right2"
                    self.originalImage=self.image
                    vehicles[self.direction][self.lane].append(self)
                    self.index = len(vehicles[self.direction][self.lane]) - 1
                    if(len(vehicles[self.direction][self.lane])>1 and vehicles[self.direction][self.lane][self.index-1].crossed==0):
                        self.stopright2=vehicles["right2"][lane][self.index-1].stop - vehicles["right2"][lane][self.index-1].image.get_rect().width - stoppingGap
                    else:
                        self.stopright2=defaultStop[self.direction]
                    self.pathchanged=1
                    
            if(self.willTurn==1):
                if(self.lane == 1):
                    if(self.crossed==0 or self.x+self.image.get_rect().width<stopLines[self.direction]+10):
                        if((self.x+self.image.get_rect().width<=self.stop or (currentGreen==0 and currentYellow==0) or self.crossed==1) and (self.index==0 or self.x+self.image.get_rect().width<(vehicles[self.direction][self.lane][self.index-1].x - movingGap) or vehicles[self.direction][self.lane][self.index-1].turned==1)):               
                            self.x += self.speed
                    else:
                        if(self.turned==0):
                            self.rotateAngle += rotationAngle
                            self.image = pygame.transform.rotate(self.originalImage, self.rotateAngle)
                            self.x += 1.5
                            self.y -= 2.0
                            if(self.rotateAngle==90):
                                self.turned = 1
                                vehiclesTurned[self.direction][self.lane].append(self)
                                self.crossedIndex = len(vehiclesTurned[self.direction][self.lane]) - 1
                        else:
                            if(self.crossedIndex==0 or (self.y>(vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].y + vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].image.get_rect().height + movingGap))):
                            
                                self.y -= self.speed
                elif(self.lane == 2):
                    if(self.crossed==0 or self.x+self.image.get_rect().width<mid[self.direction]['x']):
                        if((self.x+self.image.get_rect().width<=self.stop or (currentGreen==0 and currentYellow==0) or self.crossed==1) and (self.index==0 or self.x+self.image.get_rect().width<(vehicles[self.direction][self.lane][self.index-1].x - movingGap) or vehicles[self.direction][self.lane][self.index-1].turned==1)):                 
                            self.x += self.speed
                    else:
                        if(self.turned==0):
                            self.rotateAngle += rotationAngle
                            self.image = pygame.transform.rotate(self.originalImage, -self.rotateAngle)
                            self.x += 2
                            self.y += 1.5
                            if(self.rotateAngle==90):
                                self.turned = 1
                                vehiclesTurned[self.direction][self.lane].append(self)
                                self.crossedIndex = len(vehiclesTurned[self.direction][self.lane]) - 1
                        else:
                            if(self.crossedIndex==0 or ((self.y+self.image.get_rect().height)<(vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].y - movingGap))):
                                self.y += self.speed
            else:

                if(self.crossed == 0):
                    if((self.x+self.image.get_rect().width<=self.stop or (currentGreen==0 and currentYellow==0)) and (self.index==0 or self.x+self.image.get_rect().width<(vehicles[self.direction][self.lane][self.index-1].x - movingGap))):                
                        self.x += self.speed
                else:
                    if(self.pathchanged==1):
                       self.x += self.speed
                    else:
                        if((self.crossedIndex==0) or (self.x+self.image.get_rect().width<(vehiclesNotTurned[self.direction][self.lane][self.crossedIndex-1].x - movingGap))):                 
                            self.x += self.speed

        elif(self.direction=='right2'):
            
            if(self.crossed2==0 and self.x+self.image.get_rect().width>stopLines[self.direction]):
                self.crossed2 = 1
                vehicles[self.direction]['crossed'] += 1
                
                if(self.willTurn2==0):
                    vehiclesNotTurned[self.direction][self.lane].append(self)
                    self.crossedIndex2 = len(vehiclesNotTurned[self.direction][self.lane]) - 1
            if(self.willTurn2==1):
                if(self.lane == 1):
                    if(self.crossed2==0 or self.x+self.image.get_rect().width<stopLines[self.direction]+30):
                    
                        if((self.x+self.image.get_rect().width<=self.stopright2 or (currentGreen2==0 and currentYellow2==0) or self.crossed2==1) and (self.index==0 or self.x+self.image.get_rect().width<(vehicles[self.direction][self.lane][self.index-1].x - movingGap) or vehicles[self.direction][self.lane][self.index-1].turned2==1)):                
                            self.x += self.speed
                      
                    else:
                        
                        if(self.turned2==0):
                            self.rotateAngle2 += rotationAngle
                            self.image = pygame.transform.rotate(self.originalImage, self.rotateAngle2)
                            self.x += 1.0
                            self.y -= 2.0
                            if(self.rotateAngle2==90):
                                self.turned2 = 1
                        
                                vehiclesTurned[self.direction][self.lane].append(self)
                                self.crossedIndex2 = len(vehiclesTurned[self.direction][self.lane]) - 1
                        else:
                            if(self.crossedIndex2==0 or (self.y>(vehiclesTurned[self.direction][self.lane][self.crossedIndex2-1].y + vehiclesTurned[self.direction][self.lane][self.crossedIndex2-1].image.get_rect().height + movingGap))):
                                self.y -= self.speed
            
                elif(self.lane == 2):
                    if(self.crossed2==0 or self.x+self.image.get_rect().width<mid[self.direction]['x']):
                        if((self.x+self.image.get_rect().width<=self.stopright2 or (currentGreen2==0 and currentYellow2==0) or self.crossed2==1) and (self.index==0 or self.x+self.image.get_rect().width<(vehicles[self.direction][self.lane][self.index-1].x - movingGap) or vehicles[self.direction][self.lane][self.index-1].turned2==1)):                 
                            self.x += self.speed
                    else:
                        if(self.turned2==0):
                            self.rotateAngle2 += rotationAngle
                            self.image = pygame.transform.rotate(self.originalImage, -self.rotateAngle2)
                            self.x += 2
                            self.y += 1.5
                            if(self.rotateAngle2==90):
                                self.turned2 = 1
                                vehiclesTurned[self.direction][self.lane].append(self)
                                self.crossedIndex2 = len(vehiclesTurned[self.direction][self.lane]) - 1
                        else:
                            if(self.crossedIndex2==0 or ((self.y+self.image.get_rect().height)<(vehiclesTurned[self.direction][self.lane][self.crossedIndex2-1].y - movingGap))):
                                self.y += self.speed
       
            else:
                
                if(self.crossed2 == 0):
                    
                    if((self.x+self.image.get_rect().width<=self.stopright2 or (currentGreen2==0 and currentYellow2==0)) and (self.index==0 or self.x+self.image.get_rect().width<(vehicles[self.direction][self.lane][self.index-1].x - movingGap))):                
                        self.x += self.speed
                else:
                   
                    if((self.crossedIndex2==0)or (self.crossedIndex2==-1) or (self.x+self.image.get_rect().width<(vehiclesNotTurned[self.direction][self.lane][self.crossedIndex2-1].x - movingGap))):                 
                        self.x += self.speed

        elif(self.direction=='down'):
            if(self.crossed==0 and self.y+self.image.get_rect().height>stopLines[self.direction]):
                self.crossed = 1
                
                vehicles[self.direction]['crossed'] += 1
                if(self.willTurn==0):
                    vehiclesNotTurned[self.direction][self.lane].append(self)
                    self.crossedIndex = len(vehiclesNotTurned[self.direction][self.lane]) - 1
            if(self.willTurn==1):
                if(self.lane == 1):
                  
                        
                    if(self.crossed==0 or self.y+self.image.get_rect().height<stopLines[self.direction]+10):
                       
                        if((self.y+self.image.get_rect().height<=self.stop or (currentGreen==1 and currentYellow==0) or self.crossed==1) and (self.index==0 or self.y+self.image.get_rect().height<(vehicles[self.direction][self.lane][self.index-1].y - movingGap) or vehicles[self.direction][self.lane][self.index-1].turned==1)):                
                            self.y += self.speed
                           
                    else: 
                        if(self.turned==0):
                            self.rotateAngle += rotationAngle
                            self.image = pygame.transform.rotate(self.originalImage, self.rotateAngle)
                            self.x += 0.9
                            self.y += 1.9
                            if(self.rotateAngle==90):
                                self.turned = 1
                                vehiclesTurned[self.direction][self.lane].append(self)
                                self.crossedIndex = len(vehiclesTurned[self.direction][self.lane]) - 1

                        
                                self.direction="right2"
                                self.originalImage=self.image
                                vehicles[self.direction][self.lane].append(self)
                                self.index = len(vehicles[self.direction][self.lane]) - 1
                                if(len(vehicles[self.direction][self.lane])>1 and vehicles[self.direction][self.lane][self.index-1].crossed==0):
                                    self.stopright2=vehicles["right2"][lane][self.index-1].stop - vehicles["right2"][lane][self.index-1].image.get_rect().width - stoppingGap
                                else:
                                    self.stopright2=defaultStop[self.direction]
                                    
                        else:
                            if(self.crossedIndex==0 or ((self.x + self.image.get_rect().width) < (vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].x - movingGap))):
                                self.x += self.speed
                elif(self.lane == 2):
                    if(self.crossed==0 or self.y+self.image.get_rect().height<mid[self.direction]['y']):
                        if((self.y+self.image.get_rect().height<=self.stop or (currentGreen==1 and currentYellow==0) or self.crossed==1) and (self.index==0 or self.y+self.image.get_rect().height<(vehicles[self.direction][self.lane][self.index-1].y - movingGap) or vehicles[self.direction][self.lane][self.index-1].turned==1)):                
                            self.y += self.speed
                    else:   
                        if(self.turned==0):
                            self.rotateAngle += rotationAngle
                            self.image = pygame.transform.rotate(self.originalImage, -self.rotateAngle)
                            self.x -= 2.2
                            self.y += 1.7
                            if(self.rotateAngle==90):
                                self.turned = 1
                                vehiclesTurned[self.direction][self.lane].append(self)
                                self.crossedIndex = len(vehiclesTurned[self.direction][self.lane]) - 1

                                
                                
                        else:
                            if(self.crossedIndex==0 or (self.x>(vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].x + vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].image.get_rect().width + movingGap))): 
                                self.x -= self.speed
            
            else:
            
                if(self.crossed == 0):
                
                    if((self.y+self.image.get_rect().height<=self.stop or (currentGreen==1 and currentYellow==0)) and (self.index==0 or self.y+self.image.get_rect().height<(vehicles[self.direction][self.lane][self.index-1].y - movingGap))):                
                        self.y += self.speed
                        
                else:
                    if((self.crossedIndex==0) or (self.y+self.image.get_rect().height<(vehiclesNotTurned[self.direction][self.lane][self.crossedIndex-1].y - movingGap))):                
                        self.y += self.speed
        ################################################
        elif(self.direction=='down2'):
            if(self.crossed==0 and self.y+self.image.get_rect().height>stopLines[self.direction]):
                self.crossed = 1
                vehicles[self.direction]['crossed'] += 1
                if(self.willTurn==0):
                    vehiclesNotTurned[self.direction][self.lane].append(self)
                    self.crossedIndex = len(vehiclesNotTurned[self.direction][self.lane]) - 1
            if(self.willTurn==1):

                if(self.lane == 1):
                    if(self.crossed==0 or self.y+self.image.get_rect().height<stopLines[self.direction]+10):
                        if((self.y+self.image.get_rect().height<=self.stop or (currentGreen2==1 and currentYellow2==0) or self.crossed==1) and (self.index==0 or self.y+self.image.get_rect().height<(vehicles[self.direction][self.lane][self.index-1].y - movingGap) or vehicles[self.direction][self.lane][self.index-1].turned==1)):                
                            self.y += self.speed
                    else:   
                        if(self.turned==0):
                            self.rotateAngle += rotationAngle
                            self.image = pygame.transform.rotate(self.originalImage, self.rotateAngle)
                            self.x += 1.2
                            self.y += 1.5
                            if(self.rotateAngle==90):
                                self.turned = 1
                                vehiclesTurned[self.direction][self.lane].append(self)
                                self.crossedIndex = len(vehiclesTurned[self.direction][self.lane]) - 1

                               
                        else:
                            if(self.crossedIndex==0 or ((self.x + self.image.get_rect().width) < (vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].x - movingGap))):
                                self.x += self.speed
                elif(self.lane == 2):
                    if(self.crossed==0 or self.y+self.image.get_rect().height<mid[self.direction]['y']):
                        if((self.y+self.image.get_rect().height<=self.stop or (currentGreen2==1 and currentYellow2==0) or self.crossed==1) and (self.index==0 or self.y+self.image.get_rect().height<(vehicles[self.direction][self.lane][self.index-1].y - movingGap) or vehicles[self.direction][self.lane][self.index-1].turned==1)):                
                            self.y += self.speed
                    else:   
                        if(self.turned==0):
                            self.rotateAngle += rotationAngle
                            self.image = pygame.transform.rotate(self.originalImage, -self.rotateAngle)
                            self.x -= 1
                            self.y += 1.4
                            if(self.rotateAngle==90):
                                self.turned = 1
                                vehiclesTurned[self.direction][self.lane].append(self)
                                self.crossedIndex = len(vehiclesTurned[self.direction][self.lane]) - 1

                                self.direction="left2"
                                self.originalImage=self.image
                                vehicles[self.direction][self.lane].append(self)
                                self.index = len(vehicles[self.direction][self.lane]) - 1
                                if(len(vehicles[self.direction][self.lane])>1 and vehicles[self.direction][self.lane][self.index-1].crossed==0):
                                    self.stopleft2=vehicles["left2"][lane][self.index-1].stop - vehicles["left2"][lane][self.index-1].image.get_rect().width - stoppingGap
                                else:
                                    self.stopleft2=defaultStop[self.direction]
                        else:
                            if(self.crossedIndex==0 or (self.x>(vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].x + vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].image.get_rect().width + movingGap))): 
                                self.x -= self.speed
            else: 
                if(self.crossed == 0):
                    if((self.y+self.image.get_rect().height<=self.stop or (currentGreen2==1 and currentYellow2==0)) and (self.index==0 or self.y+self.image.get_rect().height<(vehicles[self.direction][self.lane][self.index-1].y - movingGap))):                
                        self.y += self.speed
                else:
                    if((self.crossedIndex==0) or (self.y+self.image.get_rect().height<(vehiclesNotTurned[self.direction][self.lane][self.crossedIndex-1].y - movingGap))):                
                        self.y += self.speed
        ########################################################
        elif(self.direction=='left'):
            if(self.crossed==0 and self.x<stopLines[self.direction]):
                self.crossed = 1
                vehicles[self.direction]['crossed'] += 1
                if(self.willTurn==0):
                    vehiclesNotTurned[self.direction][self.lane].append(self)
                    self.crossedIndex = len(vehiclesNotTurned[self.direction][self.lane]) - 1
                    
                    self.direction="left2"
                    self.originalImage=self.image
                    vehicles[self.direction][self.lane].append(self)
                    self.index = len(vehicles[self.direction][self.lane]) - 1
                    if(len(vehicles[self.direction][self.lane])>1 and vehicles[self.direction][self.lane][self.index-1].crossed==0):
                        self.stopleft2=vehicles["left2"][lane][self.index-1].stop - vehicles["left2"][lane][self.index-1].image.get_rect().width - stoppingGap
                    else:
                        self.stopleft2=defaultStop[self.direction]
                    self.pathchanged=1

                    
                    
            if(self.willTurn==1):
                if(self.lane == 1):
                    if(self.crossed==0 or self.x>stopLines[self.direction]-10):
                        if((self.x>=self.stop or (currentGreen2==2 and currentYellow2==0) or self.crossed==1) and (self.index==0 or self.x>(vehicles[self.direction][self.lane][self.index-1].x + vehicles[self.direction][self.lane][self.index-1].image.get_rect().width + movingGap) or vehicles[self.direction][self.lane][self.index-1].turned==1)):                
                            self.x -= self.speed
                    else: 
                        if(self.turned==0):
                            self.rotateAngle += rotationAngle
                            self.image = pygame.transform.rotate(self.originalImage, self.rotateAngle)
                            self.x -= 1
                            self.y += 1.2
                            if(self.rotateAngle==90):
                                self.turned = 1
                                vehiclesTurned[self.direction][self.lane].append(self)
                                self.crossedIndex = len(vehiclesTurned[self.direction][self.lane]) - 1
                        else:
                            if(self.crossedIndex==0 or ((self.y + self.image.get_rect().height) <(vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].y  -  movingGap))):
                                self.y += self.speed
                elif(self.lane == 2):
                    if(self.crossed==0 or self.x>mid[self.direction]['x']):
                        if((self.x>=self.stop or (currentGreen2==2 and currentYellow2==0) or self.crossed==1) and (self.index==0 or self.x>(vehicles[self.direction][self.lane][self.index-1].x + vehicles[self.direction][self.lane][self.index-1].image.get_rect().width + movingGap) or vehicles[self.direction][self.lane][self.index-1].turned==1)):                
                            self.x -= self.speed
                    else:
                        if(self.turned==0):
                            self.rotateAngle += rotationAngle
                            self.image = pygame.transform.rotate(self.originalImage, -self.rotateAngle)
                            self.x -= 1.8
                            self.y -= 2.5
                            if(self.rotateAngle==90):
                                self.turned = 1
                                vehiclesTurned[self.direction][self.lane].append(self)
                                self.crossedIndex = len(vehiclesTurned[self.direction][self.lane]) - 1
                        else:
                            if(self.crossedIndex==0 or (self.y>(vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].y + vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].image.get_rect().height +  movingGap))):
                                self.y -= self.speed
            else:
    
                if(self.crossed == 0):
                    if((self.x>=self.stop or (currentGreen2==2 and currentYellow2==0)) and (self.index==0 or self.x>(vehicles[self.direction][self.lane][self.index-1].x + vehicles[self.direction][self.lane][self.index-1].image.get_rect().width + movingGap))):
                        self.x -= self.speed
                else:
                
                    if(self.pathchanged==0):
                        print('g')
                        if((self.crossedIndex==0) or (self.x>(vehiclesNotTurned[self.direction][self.lane][self.crossedIndex-1].x + vehiclesNotTurned[self.direction][self.lane][self.crossedIndex-1].image.get_rect().width + movingGap))):                
                            self.x -= self.speed
                            
        elif(self.direction=='left2'):
            if(self.crossed2==0 and self.x<stopLines[self.direction]):
                
                self.crossed2 = 1
                vehicles[self.direction]['crossed'] += 1
                if(self.willTurn2==0):
                    vehiclesNotTurned[self.direction][self.lane].append(self)
                    self.crossedIndex2 = len(vehiclesNotTurned[self.direction][self.lane]) - 1
            if(self.willTurn2==1):
                
                if(self.lane == 1):
                    if(self.crossed2==0 or self.x>stopLines[self.direction]-10):
                        if((self.x>=self.stopleft2 or (currentGreen==2 and currentYellow==0) or self.crossed2==1) and (self.index==0 or self.x>(vehicles[self.direction][self.lane][self.index-1].x + vehicles[self.direction][self.lane][self.index-1].image.get_rect().width + movingGap) or vehicles[self.direction][self.lane][self.index-1].turned2==1)):                
                            self.x -= self.speed
                    else:
                        if(self.turned2==0):
                            self.rotateAngle2 += rotationAngle
                            self.image = pygame.transform.rotate(self.originalImage, self.rotateAngle2)
                            self.x -= 1
                            self.y += 1.2
                            if(self.rotateAngle2==90):
                                self.turned2 = 1
                                vehiclesTurned[self.direction][self.lane].append(self)
                                self.crossedIndex2 = len(vehiclesTurned[self.direction][self.lane]) - 1
                        else:
                            if(self.crossedIndex2==0 or ((self.y + self.image.get_rect().height) <(vehiclesTurned[self.direction][self.lane][self.crossedIndex2-1].y  -  movingGap))):
                                self.y += self.speed
                elif(self.lane == 2):
                    if(self.crossed2==0 or self.x>mid[self.direction]['x']):

                        if((self.x>=self.stopleft2 or (currentGreen==2 and currentYellow==0) or self.crossed2==1) and (self.index==0 or self.x>(vehicles[self.direction][self.lane][self.index-1].x + vehicles[self.direction][self.lane][self.index-1].image.get_rect().width + movingGap) or vehicles[self.direction][self.lane][self.index-1].turned2==1)):                
                            self.x -= self.speed
                    else:
            
                        if(self.turned2==0):
                            self.rotateAngle2 += rotationAngle
                            self.image = pygame.transform.rotate(self.originalImage, -self.rotateAngle2)
                            self.x -= 1.8
                            self.y -= 2.5
                            if(self.rotateAngle2==90):
                                self.turned2 = 1
                                vehiclesTurned[self.direction][self.lane].append(self)
                                self.crossedIndex2 = len(vehiclesTurned[self.direction][self.lane]) - 1
                        else:
                            if(self.crossedIndex2==0 or (self.y>(vehiclesTurned[self.direction][self.lane][self.crossedIndex2-1].y + vehiclesTurned[self.direction][self.lane][self.crossedIndex2-1].image.get_rect().height +  movingGap))):
                                self.y -= self.speed
            else:
                if(self.crossed2 == 0):
                    if((self.x>=self.stopleft2 or (currentGreen==2 and currentYellow==0)) and (self.index==0 or self.x>(vehicles[self.direction][self.lane][self.index-1].x + vehicles[self.direction][self.lane][self.index-1].image.get_rect().width + movingGap))):                
                        self.x -= self.speed
                else:
                    if((self.crossedIndex2==0)or (self.crossedIndex2==-1) or (self.x>(vehiclesNotTurned[self.direction][self.lane][self.crossedIndex2-1].x + vehiclesNotTurned[self.direction][self.lane][self.crossedIndex2-1].image.get_rect().width + movingGap))):                
                        self.x -= self.speed

                        
        elif(self.direction=='up'):
            if(self.crossed==0 and self.y<stopLines[self.direction]):
                self.crossed = 1
                vehicles[self.direction]['crossed'] += 1
                if(self.willTurn==0):
                    vehiclesNotTurned[self.direction][self.lane].append(self)
                    self.crossedIndex = len(vehiclesNotTurned[self.direction][self.lane]) - 1
            if(self.willTurn==1):
                if(self.lane == 1):
                    if(self.crossed==0 or self.y>stopLines[self.direction]-5):
                        if((self.y>=self.stop or (currentGreen==3 and currentYellow==0) or self.crossed == 1) and (self.index==0 or self.y>(vehicles[self.direction][self.lane][self.index-1].y + vehicles[self.direction][self.lane][self.index-1].image.get_rect().height +  movingGap) or vehicles[self.direction][self.lane][self.index-1].turned==1)):
                            self.y -= self.speed
                    else:   
                        if(self.turned==0):
                            self.rotateAngle += rotationAngle
                            self.image = pygame.transform.rotate(self.originalImage, self.rotateAngle)
                            self.x -= 1
                            self.y -= 1
                            if(self.rotateAngle==90):
                                self.turned = 1
                                vehiclesTurned[self.direction][self.lane].append(self)
                                self.crossedIndex = len(vehiclesTurned[self.direction][self.lane]) - 1
                        else:
                            if(self.crossedIndex==0 or (self.x>(vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].x + vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].image.get_rect().width + movingGap))):
                                self.x -= self.speed
                elif(self.lane == 2):
                    if(self.crossed==0 or self.y>mid[self.direction]['y']):
                        if((self.y>=self.stop or (currentGreen==3 and currentYellow==0) or self.crossed == 1) and (self.index==0 or self.y>(vehicles[self.direction][self.lane][self.index-1].y + vehicles[self.direction][self.lane][self.index-1].image.get_rect().height +  movingGap) or vehicles[self.direction][self.lane][self.index-1].turned==1)):
                            self.y -= self.speed
                    else:   
                        if(self.turned==0):
                            self.rotateAngle += rotationAngle
                            self.image = pygame.transform.rotate(self.originalImage, -self.rotateAngle)
                            self.x += 1
                            self.y -= 1
                            if(self.rotateAngle==90):
                                self.turned = 1
                                vehiclesTurned[self.direction][self.lane].append(self)
                                self.crossedIndex = len(vehiclesTurned[self.direction][self.lane]) - 1

                                self.direction="right2"
                                self.originalImage=self.image
                                vehicles[self.direction][self.lane].append(self)
                                self.index = len(vehicles[self.direction][self.lane]) - 1
                                if(len(vehicles[self.direction][self.lane])>1 and vehicles[self.direction][self.lane][self.index-1].crossed==0):
                                    self.stopright2=vehicles["right2"][lane][self.index-1].stop - vehicles["right2"][lane][self.index-1].image.get_rect().width - stoppingGap
                                else:
                                    self.stopright2=defaultStop[self.direction]
                                    
                        else:
                            if(self.crossedIndex==0 or (self.x<(vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].x - vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].image.get_rect().width - movingGap))):
                                self.x += self.speed
            else: 
                if(self.crossed == 0):
                    if((self.y>=self.stop or (currentGreen==3 and currentYellow==0)) and (self.index==0 or self.y>(vehicles[self.direction][self.lane][self.index-1].y + vehicles[self.direction][self.lane][self.index-1].image.get_rect().height + movingGap))):                
                        self.y -= self.speed
                else:
                    if((self.crossedIndex==0) or (self.y>(vehiclesNotTurned[self.direction][self.lane][self.crossedIndex-1].y + vehiclesNotTurned[self.direction][self.lane][self.crossedIndex-1].image.get_rect().height + movingGap))):                
                        self.y -= self.speed 

        elif(self.direction=='up2'):
            
            if(self.crossed==0 and self.y<stopLines[self.direction]):
                self.crossed = 1
                vehicles[self.direction]['crossed'] += 1
             
                if(self.willTurn==0):
                    vehiclesNotTurned[self.direction][self.lane].append(self)
                    self.crossedIndex = len(vehiclesNotTurned[self.direction][self.lane]) - 1
            if(self.willTurn==1):
                if(self.lane == 1):
                    if(self.crossed==0 or self.y>stopLines[self.direction]-5):
                        if((self.y>=self.stop or (currentGreen2==3 and currentYellow2==0) or self.crossed == 1) and (self.index==0 or self.y>(vehicles[self.direction][self.lane][self.index-1].y + vehicles[self.direction][self.lane][self.index-1].image.get_rect().height +  movingGap) or vehicles[self.direction][self.lane][self.index-1].turned==1)):
                            self.y -= self.speed
                   
                    else:   
                        if(self.turned==0):
                            self.rotateAngle += rotationAngle
                            self.image = pygame.transform.rotate(self.originalImage, self.rotateAngle)
                            self.x -= 1.0
                            self.y -= 1
                       
                            if(self.rotateAngle==90):
                                self.turned = 1
                                vehiclesTurned[self.direction][self.lane].append(self)
                                self.crossedIndex = len(vehiclesTurned[self.direction][self.lane]) - 1

                                self.direction="left2"
                                self.originalImage=self.image
                                vehicles[self.direction][self.lane].append(self)
                                self.index = len(vehicles[self.direction][self.lane]) - 1
                                if(len(vehicles[self.direction][self.lane])>1 and vehicles[self.direction][self.lane][self.index-1].crossed==0):
                                    self.stopleft2=vehicles["left2"][lane][self.index-1].stop - vehicles["left2"][lane][self.index-1].image.get_rect().width - stoppingGap
                                else:
                                    self.stopleft2=defaultStop[self.direction]

                        else:
                            if(self.crossedIndex==0 or (self.x>(vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].x + vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].image.get_rect().width + movingGap))):
                                self.x -= self.speed
                            
                elif(self.lane == 2):
                    if(self.crossed==0 or self.y>mid[self.direction]['y']):
                        if((self.y>=self.stop or (currentGreen2==3 and currentYellow2==0) or self.crossed == 1) and (self.index==0 or self.y>(vehicles[self.direction][self.lane][self.index-1].y + vehicles[self.direction][self.lane][self.index-1].image.get_rect().height +  movingGap) or vehicles[self.direction][self.lane][self.index-1].turned==1)):
                            self.y -= self.speed
                
                    else:   
                        if(self.turned==0):
                            self.rotateAngle += rotationAngle
                            self.image = pygame.transform.rotate(self.originalImage, -self.rotateAngle)
                            self.x += 1
                            self.y -= 1
                    
                            if(self.rotateAngle==90):
                                self.turned = 1
                                vehiclesTurned[self.direction][self.lane].append(self)
                                self.crossedIndex = len(vehiclesTurned[self.direction][self.lane]) - 1
                        else:
                            if(self.crossedIndex==0 or (self.x<(vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].x - vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].image.get_rect().width - movingGap))):
                                self.x += self.speed
              
            else: 
                if(self.crossed == 0):
                    if((self.y>=self.stop or (currentGreen2==3 and currentYellow2==0)) and (self.index==0 or self.y>(vehicles[self.direction][self.lane][self.index-1].y + vehicles[self.direction][self.lane][self.index-1].image.get_rect().height + movingGap))):                
                        self.y -= self.speed
    
                else:
                    if((self.crossedIndex==0) or (self.y>(vehiclesNotTurned[self.direction][self.lane][self.crossedIndex-1].y + vehiclesNotTurned[self.direction][self.lane][self.crossedIndex-1].image.get_rect().height + movingGap))):                
                        self.y -= self.speed
          
            



# Initialization of signals with default values
def initialize():
    ts1 = TrafficSignal(0, defaultYellow, defaultGreen[0])
    signals.append(ts1)
    ts2 = TrafficSignal(ts1.yellow+ts1.green, defaultYellow, defaultGreen[1])
    signals.append(ts2)
    ts3 = TrafficSignal(defaultRed, defaultYellow, defaultGreen[2])
    signals.append(ts3)
    ts4 = TrafficSignal(defaultRed, defaultYellow, defaultGreen[3])
    signals.append(ts4)
    repeat()

def initialize2():
    ts1 = TrafficSignal(0, defaultYellow, defaultGreen2[0])
    signals2.append(ts1)
    ts2 = TrafficSignal(ts1.yellow+ts1.green, defaultYellow, defaultGreen2[1])
    signals2.append(ts2)
    ts3 = TrafficSignal(defaultRed, defaultYellow, defaultGreen2[2])
    signals2.append(ts3)
    ts4 = TrafficSignal(defaultRed, defaultYellow, defaultGreen2[3])
    signals2.append(ts4)
    repeat2()


def repeat():
    global currentGreen, currentYellow, nextGreen

    # reset all signal times of current signal to default/random times
    signals[currentGreen].green = defaultGreen[currentGreen]
    signals[currentGreen].yellow = defaultYellow
    signals[currentGreen].red = defaultRed

    nextGreen = (currentGreen+1)%noOfSignals
        
    
    
    while(signals[currentGreen].green>0):   # while the timer of current green signal is not zero
        updateValues(False)
        time.sleep(1.5)
       
    currentYellow = 1   # set yellow signal on
    # reset stop coordinates of lanes and vehicles 
    for i in range(0,3):
        for vehicle in vehicles[directionNumbers1[currentGreen]][i]:
            vehicle.stop = defaultStop[directionNumbers1[currentGreen]]

    signals[nextGreen].red = 5    # set the red time of next to next signal as (yellow time + green time) of next signal
    while(signals[currentGreen].yellow>0):  # while the timer of current yellow signal is not zero
        updateValues(True)
        time.sleep(1.5)
    
    currentYellow = 0   # set yellow signal off
    currentGreen = nextGreen # set next signal as green signal
    
    repeat()

def repeat2():
    global currentGreen2, currentYellow2, nextGreen2

    # reset all signal times of current signal to default/random times
    signals2[currentGreen2].green = defaultGreen2[currentGreen2]
    signals2[currentGreen2].yellow = defaultYellow
    signals2[currentGreen2].red = defaultRed

    nextGreen2 = (currentGreen2+1)%noOfSignals    # set next green signal
    
    while(signals2[currentGreen2].green>0):   # while the timer of current green signal is not zero
        updateValues2(False)
        time.sleep(1.5)
    currentYellow2 = 1   # set yellow signal on
    
    # reset stop coordinates of lanes and vehicles 
    for i in range(0,3):
        for vehicle in vehicles[directionNumbers2[currentGreen2]][i]:
            vehicle.stop = defaultStop[directionNumbers2[currentGreen2]]

    signals2[nextGreen2].red = 5
    
    while(signals2[currentGreen2].yellow>0):  # while the timer of current yellow signal is not zero
        updateValues2(True)
        time.sleep(1.5)

    currentYellow2 = 0   # set yellow signal off
    currentGreen2 = nextGreen2 # set next signal as green signal

    repeat2()



# Update values of the signal timers after every second


def VehicalLoadCount(light):
    load=0
    for lane in [1,2]:
        if(len(vehicles[directionNumbers1[light]][lane])!=0):
            for vehi in range(0,len(vehicles[directionNumbers1[light]][lane])):

                if(light==1):
                    if(vehicles[directionNumbers1[light]][lane][::-1][vehi].crossed==0 ):
                        if( 0<vehicles[directionNumbers1[light]][lane][::-1][vehi].y<140 ):
                            load=load+1
                    else:
                        break
                elif(light==3):
                    if(vehicles[directionNumbers1[light]][lane][::-1][vehi].crossed==0 ):
                        if( 275<vehicles[directionNumbers1[light]][lane][::-1][vehi].y<430 ):
                            load=load+1
                    else:
                        break
                elif(light==0):
                    if(vehicles[directionNumbers1[light]][lane][::-1][vehi].crossed==0 ):
                        if(0<vehicles[directionNumbers1[light]][lane][::-1][vehi].x<285 ):
                            load=load+1
                    else:
                        break
                    
                elif(light==2):
                    if(vehicles[directionNumbers1[light]][lane][::-1][vehi].crossed2==0):
                        if(410<vehicles[directionNumbers1[light]][lane][::-1][vehi].x<700):
                            load=load+1
                    else:
                        break
    
    return load


def Trafficcontroller():
    global currentGreen,nextGreen
    while True:
        vehicalcount=0
        for light in range(noOfSignals):
            if(currentGreen!=light ):
                vehicalload[light]=VehicalLoadCount(light)
                if(vehicalload[light]>8):
                    if(vehicalcount<vehicalload[light]):
                        vehicalzcount=vehicalload[light]
                
                if(0<vehicalload[light]<=4):
                    defaultGreen[light]=2
                elif(vehicalload[light]==0):
                    defaultGreen[light]=0
                elif(vehicalload[light]>4):
                    defaultGreen[light]=int(vehicalload[light]/2)
                    
                if(currentYellow==0):
                    if(vehicalload[light]>6):
                        if(vehicalcount<vehicalload[light]):
                            nextGreen=light
    
        print()

# Update values of the signal timers after every second
def VehicalLoadCount2(light2):
  
    load2=0
    for lane2 in [1,2]:
        if(len(vehicles[directionNumbers2[light2]][lane2])!=0): 
            for vehi2 in range(0,len(vehicles[directionNumbers2[light2]][lane2])):
                if(light2==1):
                    if(vehicles[directionNumbers2[light2]][lane2][::-1][vehi2].crossed==0):
                        if( 0<vehicles[directionNumbers2[light2]][lane2][::-1][vehi2].y<150):
                            load2=load2+1
                    else:
                        break
                elif(light2==2):
                    if(vehicles[directionNumbers2[light2]][lane2][::-1][vehi2].crossed==0 ):
                        if( 1110<vehicles[directionNumbers2[light2]][lane2][::-1][vehi2].x<1350):
                            load2=load2+1
                    else:
                        break
                elif(light2==3):
                    if(vehicles[directionNumbers2[light2]][lane2][::-1][vehi2].crossed==0):
                        if(275<vehicles[directionNumbers2[light2]][lane2][::-1][vehi2].y<450):
                            load2=load2+1
                    else:
                        break
                    
                elif(light2==0):
                    if(vehicles[directionNumbers2[light2]][lane2][::-1][vehi2].crossed2==0 ):
                        if( 700<vehicles[directionNumbers2[light2]][lane2][::-1][vehi2].x<1010 ):
                            load2=load2+1
                    else:
                        break
 
    return load2

def Trafficcontroller2():
    global currentGreen2,nextGreen2
    while True:
        vehicalcount2=0
        for light in range(noOfSignals2):
            if(currentGreen2!=light ):
                vehicalload2[light]=VehicalLoadCount2(light)
                if(vehicalload2[light]>8):
                    if(vehicalcount2<vehicalload2[light]):
                        vehicalcount2=vehicalload2[light]
                if(0<vehicalload2[light]<=4):
                    defaultGreen2[light]=2
                elif(vehicalload2[light]==0):
                    defaultGreen2[light]=0
                elif(vehicalload2[light]>4):
                    defaultGreen2[light]=int(vehicalload2[light]/2)
                    
                if(currentYellow2==0):
                    if(vehicalload2[light]>6):
                        if(vehicalcount2<vehicalload2[light]):
                            nextGreen2=light
        
        print()         
                        
            

        
     
            
            
def updateValues(yellowcount):
    for i in range(0, noOfSignals):
        if(i==currentGreen):
            if(currentYellow==0):
                signals[i].green-=1
            else:
                signals[i].yellow-=1
        else:
            if(yellowcount):
                signals[i].red-=1
# Update values of the signal timers after every second
def updateValues2(yellowcount):
    for i in range(0, noOfSignals):
        if(i==currentGreen2):
            if(currentYellow2==0):
                signals2[i].green-=1
            else:
                signals2[i].yellow-=1
        else:
            if(yellowcount):
                signals2[i].red-=1

# Generating vehicles in the simulation
def generateVehicles():
    #for a in range(1):
    while True:
        vehicle_type = random.choice(allowedVehicleTypesList)
        lane_number = random.randint(1,2)

        will_turn1 = random.randint(0,1)
        will_turn2 = random.randint(0,1)
        
        direction_number = random.randint(0,5)
        if(direction_number in [1,3,4,5]):
            will_turn2=0
            
        will_turn=[will_turn1,will_turn2]
        Vehicle(lane_number, vehicleTypes[vehicle_type], direction_number, directionNumbers[direction_number], will_turn)
        time.sleep(1)
        

def showStats():
    totalVehicles = 0
    print('Direction-wise Vehicle Counts')
    for i in range(0,4):
        if(signals[i]!=None):
            print('Direction',i+1,':',vehicles[directionNumbers[i]]['crossed'])
            totalVehicles += vehicles[directionNumbers[i]]['crossed']
    print('Total vehicles passed:',totalVehicles)
    print('Total time:',timeElapsed)

def simTime():
    global timeElapsed, simulationTime
    while(True):
        timeElapsed += 1
        time.sleep(1)
        if(timeElapsed==simulationTime):
            showStats()
            junctions=[directionNumbers1,directionNumbers2]
            for junction in range(2):
                vehi_count=0
                for road in range(4):
                    if(junction==0):
                        if(road!=2):
                            for lane in [1,2]:
                                for vehi in vehicles[junctions[junction][road]][lane]:
                                    if(vehi.crossed==1):
                                        vehi_count=vehi_count+1
                        else:
                            for lane in [1,2]:
                                for vehi in vehicles[junctions[junction][road]][lane]:
                                    if(vehi.crossed2==1):
                                        vehi_count=vehi_count+1
                    else:
                        if(road!=0):
                            for lane in [1,2]:
                                for vehi in vehicles[junctions[junction][road]][lane]:
                                    if(vehi.crossed==1):
                                        vehi_count=vehi_count+1
                        else:
                            for lane in [1,2]:
                                for vehi in vehicles[junctions[junction][road]][lane]:
                                    if(vehi.crossed2==1):
                                        vehi_count=vehi_count+1
                    print("Vehical pass junction ",junction+1, "road ",junctions[junction]," : ",vehi_count)
                        
            print("timeElapsed : ",simulationTime)
            os._exit(1)
 

class Main:
    global allowedVehicleTypesList
    i = 0
    for vehicleType in allowedVehicleTypes:
        if(allowedVehicleTypes[vehicleType]):
            allowedVehicleTypesList.append(i)
        i += 1

    
    
    thread5 = threading.Thread(name="Trafficcontroller",target=Trafficcontroller, args=())    
    thread5.daemon = True
    thread5.start()


    thread6 = threading.Thread(name="Trafficcontroller2",target=Trafficcontroller2, args=())    
    thread6.daemon = True
    thread6.start()

    thread1 = threading.Thread(name="initialization",target=initialize, args=())    # initialization
    thread1.daemon = True
    thread1.start()


    
    thread4 = threading.Thread(name="initialization2",target=initialize2, args=())    # initialization
    thread4.daemon = True
    thread4.start()


    
    # Colours 
    black = (0, 0, 0)
    white = (255, 255, 255)

    # Screensize 
    screenWidth = 1392
    screenHeight = 459
    #screenHeight = 1000
    screenSize = (screenWidth, screenHeight)

    # Setting background image i.e. image of intersection
    background = pygame.image.load('images/ResizedIntersection.png')

    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("SIMULATION")


    # Loading signal images and font
    redSignal = pygame.image.load('images/signals/red.png')
    yellowSignal = pygame.image.load('images/signals/yellow.png')
    greenSignal = pygame.image.load('images/signals/green.png')
    font = pygame.font.Font(None, 30)
    thread2 = threading.Thread(name="generateVehicles",target=generateVehicles, args=())    # Generating vehicles
    thread2.daemon = True
    thread2.start()

    thread3 = threading.Thread(name="simTime",target=simTime, args=()) 
    thread3.daemon = True
    thread3.start()

    
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                showStats()
                sys.exit()

        screen.blit(background,(0,0))   # display background in simulation
        for i in range(0,noOfSignals):  # display signal and set timer according to current status: green, yello, or red
            if(i==currentGreen):
                if(currentYellow==1):
                    signals[i].signalText = signals[i].yellow
                    screen.blit(yellowSignal, signalCoods_1[i])
                else:
                    signals[i].signalText = signals[i].green
                    screen.blit(greenSignal, signalCoods_1[i])
            else:
                if(signals[i].red<=4):
                    signals[i].signalText = signals[i].red
                else:
                    signals[i].signalText = "---"
                screen.blit(redSignal, signalCoods_1[i])
        

        ######################################
        for i in range(0,noOfSignals2):  # display signal and set timer according to current status: green, yello, or red
            if(i==currentGreen2):
                if(currentYellow2==1):
                    signals2[i].signalText = signals2[i].yellow
                    screen.blit(yellowSignal, signalCoods_2[i])
                else:
                    signals2[i].signalText = signals2[i].green
                    screen.blit(greenSignal, signalCoods_2[i])
            else:
                if(signals2[i].red<=10):
                    signals2[i].signalText = signals2[i].red
                else:
                    signals2[i].signalText = "---"
                screen.blit(redSignal, signalCoods_2[i])
        ###############################################

        
        
        ##############################################
        
        signalTexts = ["","","",""]

        # display signal timer
        for i in range(0,noOfSignals):  
            signalTexts[i] = font.render(str(signals[i].signalText), True, white, black)
            screen.blit(signalTexts[i],signalTimerCoods_1[i])

        # display signal timer
        for i in range(0,noOfSignals):  
            signalTexts[i] = font.render(str(signals2[i].signalText), True, white, black)
            screen.blit(signalTexts[i],signalTimerCoods_2[i])

         # display vehicle count
        for i in range(0,noOfSignals):
            displayText =vehicalload[i]
            vehicleCountTexts[i] = font.render(str(displayText), True, black, white)
            screen.blit(vehicleCountTexts[i],vehicleCountCoods[i])

        # display vehicle2 count
        for i in range(0,noOfSignals):
            displayText = vehicalload2[i]
            vehicleCountTexts2[i] = font.render(str(displayText), True, black, white)
            screen.blit(vehicleCountTexts2[i],vehicleCountCoods2[i])

  

        # display time elapsed
        timeElapsedText = font.render(("Time Elapsed: "+ str(timeElapsed)), True, black, white)
        screen.blit(timeElapsedText,timeElapsedCoods)

  
        
        # display the vehicles
        for vehicle in simulation:  
            screen.blit(vehicle.image, [vehicle.x, vehicle.y])
            vehicle.move()
            
        pygame.display.update()

Main()
