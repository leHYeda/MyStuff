import pygame
from pygame.sprite import Sprite
from random import randint

class Bullet(Sprite):
    def __init__(self, GameManager) -> None:
        super().__init__()
        self.ship= GameManager.ship
        self.screen= GameManager.screen
        self.settings= GameManager.settings
        self.color= self.settings.bulletcolor
        self.rect= pygame.Rect(0,0, self.settings.bulletsize, self.settings.bulletsize)
        self.rect.left= GameManager.ship.rect.left
        self.fire_correction(self.ship.orientation)
        self.CONSTORIENTATIOn= True
        self.orientationmatch= 0

    def update(self, orientation) -> None:
        if self.CONSTORIENTATIOn == True:
            self.orientationmatch= orientation
            self.CONSTORIENTATIOn= False
        match self.orientationmatch:
            case 0:
                self.rect.x+= self.settings.bulletspeed
            case 1:
                self.rect.y+= self.settings.bulletspeed
            case 2:
                self.rect.x-= self.settings.bulletspeed
            case 3:
                self.rect.y-= self.settings.bulletspeed
            case 4:
                self.rect.x+= self.settings.diagonalbulletspeed
                self.rect.y-= self.settings.diagonalbulletspeed
            case 5:
                self.rect.x+= self.settings.diagonalbulletspeed
                self.rect.y+= self.settings.diagonalbulletspeed
            case 6:
                self.rect.x-= self.settings.diagonalbulletspeed
                self.rect.y-= self.settings.diagonalbulletspeed
            case 7:
                self.rect.x-= self.settings.diagonalbulletspeed
                self.rect.y+= self.settings.diagonalbulletspeed
    def fire_correction(self, orientation):
        match orientation:
            case 0:
                self.rect.y= self.ship.rect.y + 122.0
                self.rect.x= self.ship.rect.x + 152.5
            case 1:
                self.rect.y= self.ship.rect.y + 162.0
                self.rect.x= self.ship.rect.x + 122.5  
            case 2:
                self.rect.y= self.ship.rect.y + 122.0
                self.rect.x= self.ship.rect.x + 92.5
            case 3:
                self.rect.y= self.ship.rect.y + 82.0
                self.rect.x= self.ship.rect.x + 122.5
            case 4:
                self.rect.y= self.ship.rect.y + 102.0
                self.rect.x= self.ship.rect.x + 142.5
            case 5:
                self.rect.y= self.ship.rect.y + 142.0
                self.rect.x= self.ship.rect.x + 142.5
            case 6:
                self.rect.y= self.ship.rect.y + 102.0
                self.rect.x= self.ship.rect.x + 102.5
            case 7:
                self.rect.y= self.ship.rect.y + 142.0
                self.rect.x= self.ship.rect.x + 102.5
    
    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

class Cannon(Sprite):
    def __init__(self, Manager):
        super().__init__()
        self.settings= Manager.settings
        self.screen= Manager.screen
        self.ship= Manager.ship
        self.rect= pygame.Rect(0,0 , 50, 20) 
        self.rect.x= 5
        self.rect.y= self.ship.rect.y
        self.cannonFollowState= True

    def draw_cannon(self):
        if self.cannonFollowState:
            self.rect.y= self.ship.rect.y+ 115
        else:
            self.rect.x+= 20
            
        pygame.draw.rect(self.screen, (randint(25, 250), randint(25, 250), randint(25, 250)), self.rect)