import pygame
from math import sqrt
class Settings:
    def __init__(self) -> None:
        self.screenwidth= 1250
        self.screenheigh= 800
        self.bg_color= (0,0,0)
        self.speed= 8
        self.bulletspeed= 30
        self.bulletsize= 6
        self.bulletcolor= (200, 200, 200)
        self.maximumbullets= 1
        self.diagonalbulletspeed= 0
        self.diagonalshipspeed= 0
        self.shieldcolor= (120, 50, 0)
        self.shieldcellsize= 24
        self.QotileSpeed= 2
        self.QotileLaunchSpeed= 15
        self.EatingOffset= 15
        self.followerSpeed= 4

    def findingSpeed(self):
        calculation= 0
        number= 1
        while True:
            calculation= sqrt(number**2 + number**2)
            if calculation <= self.bulletspeed-0.5:
                number+=1
            else:
                self.diagonalbulletspeed= number
                break
    def findingSpeedShip(self):
        calculation= 0
        number= 1
        while True:
            calculation= sqrt(number**2 + number**2)
            if calculation <= self.speed-0.5:
                number+=1
            else:
                self.diagonalshipspeed= number
                break