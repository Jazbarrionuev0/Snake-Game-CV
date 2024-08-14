import math
import random


import cvzone
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector


cap = cv2.VideoCapture(0)


cap.set(3, 1280)
cap.set(4, 720)


detector = HandDetector(detectionCon=0.8, maxHands=1)


class SnakeGameClass:
   def __init__(self, pathFood):
       self.score = 0
       self.points = []
       self.lengths = []
       self.currentLength = 0
       self.allowedLength = 150
       self.previousHead = 0,0


       self.imgFood = cv2.imread(pathFood, cv2.IMREAD_UNCHANGED)
       self.hFood, self.wFood, _= self.imgFood.shape
       self.foodPoints = 0, 0
       self.randomFoodLocation()


   def randomFoodLocation(self):
       self.foodPoints =  random.randint(100, 1000), random.randint(100, 600)


   def update(self, imgMain, currentHead):
       px, py = self.previousHead
       cx, cy = currentHead


       self.points.append([cx, cy])
       distance = math.hypot(cx-px, cy-py)
       self.lengths.append(distance)
       self.currentLength += distance
       self.previousHead = cx, cy


       if self.currentLength > self.allowedLength:
           for i, length in enumerate(self.lengths):
               self.currentLength -= length
               self.lengths.pop(i)
               self.points.pop(i)


               if self.currentLength < self.allowedLength:
                   break


       rx, ry = self.foodPoints
       if rx - self.wFood//2 < cx < rx + self.wFood//2 and ry-self.hFood//2 < cy < ry + self.hFood//2:
           self.randomFoodLocation()
           self.allowedLength += 50
           self.score += 1
           print(self.score)


       # Snake
       if self.points:
           for i, point in enumerate(self.points):
               if i !=0:
                   cv2.line(imgMain, self.points[i-1], self.points[i], (0,128,0), 20)
           cv2.circle(imgMain, self.points[-1], 20, (200,0,200), cv2.FILLED)


       # Food


       imgMain = cvzone.overlayPNG(imgMain, self.imgFood, (rx-self.wFood//2, ry-self.hFood//2))


       return imgMain




game = SnakeGameClass("Donut.png")


while True:
   success, img = cap.read()
   img = cv2.flip(img, 1)
   hands, img = detector.findHands(img, flipType=False)


   if hands:
       lmList = hands[0]['lmList']
       pointIndex = lmList[8][0:2]
       img = game.update(img, pointIndex)


   cv2.imshow('Image', img)
   cv2.waitKey(1)
