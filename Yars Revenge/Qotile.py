import pygame
from pygame.sprite import Sprite
from random import choice
from time import time
from math import sqrt
from math import atan2, sin, cos

class Qotile:
    def __init__(self, Manager) -> None:
        paths= ["yarSprites\\Qotile swirl\\l0_sprite_1.png", "yarSprites\\Qotile swirl\\l0_sprite_2.png", "yarSprites\\Qotile swirl\\l0_sprite_3.png"]
        self.screen_rect= Manager.screen.get_rect()
        self.settings= Manager.settings
        self.ship= Manager.ship
        self.initial_rect= self.screen_rect
        self.image= pygame.image.load("yarSprites\\Hive.png")
        self.swirl= [pygame.image.load(path) for path in paths]
        self.rect= self.image.get_rect()
        self.rect.centery= self.initial_rect.centery
        self.rect.right= self.initial_rect.right+90
        self.directionBox= self.image.get_rect()
        self.directionBox.centery= self.initial_rect.centery
        self.directionBox.right= self.initial_rect.right+90
        self.color= [0, 0, 0]
        self.box= pygame.Rect(self.rect.x+90, self.rect.y+85, 65, 70)
        self.pivotY= self.rect.y+109
        self.pivotX= self.rect.x+68
        self.gridN= self.settings.shieldcellsize
        self.counter= 1
        self.swirlStage= 0
        self.attackingStage= 1
        self.agressionLevel= 0.0
        self.launch_tuple= self._calculate_QotileLaunch()
        self.traveledDistance= 0
        self.QotileShields= pygame.sprite.Group()
        self.launchtimer= float(time())
        self.time_until_launch= 0
        self._shieldGenerate(Manager)
        #Every cell position
        self.shieldPositions= [(self.pivotX- self.gridN*2, self.pivotY), (self.pivotX-self.gridN*2, self.pivotY+self.gridN), (self.pivotX-self.gridN*2, self.pivotY-self.gridN),
                               (self.pivotX- self.gridN*3, self.pivotY), (self.pivotX-self.gridN*3, self.pivotY+self.gridN), (self.pivotX-self.gridN*3, self.pivotY-self.gridN),
                               (self.pivotX- self.gridN*4, self.pivotY), (self.pivotX-self.gridN*4, self.pivotY+self.gridN), (self.pivotX-self.gridN*4, self.pivotY-self.gridN),
                               (self.pivotX- self.gridN*5, self.pivotY), (self.pivotX-self.gridN*5, self.pivotY+self.gridN), (self.pivotX-self.gridN*5, self.pivotY-self.gridN),
                               (self.pivotX- self.gridN*6, self.pivotY), (self.pivotX-self.gridN*6, self.pivotY+self.gridN), (self.pivotX-self.gridN*6, self.pivotY-self.gridN),
                               (self.pivotX- self.gridN*2, self.pivotY- self.gridN*2), (self.pivotX- self.gridN*3, self.pivotY- self.gridN*2), (self.pivotX- self.gridN*4, self.pivotY- self.gridN*2),
                               (self.pivotX- self.gridN*5, self.pivotY- self.gridN*2), (self.pivotX- self.gridN*6, self.pivotY- self.gridN*2), 
                               (self.pivotX- self.gridN*2, self.pivotY+ self.gridN*2), (self.pivotX- self.gridN*3, self.pivotY+ self.gridN*2), (self.pivotX- self.gridN*4, self.pivotY+ self.gridN*2),
                               (self.pivotX- self.gridN*5, self.pivotY+ self.gridN*2), (self.pivotX- self.gridN*6, self.pivotY+ self.gridN*2),
                               (self.pivotX- self.gridN*1, self.pivotY- self.gridN*3), (self.pivotX- self.gridN*2, self.pivotY- self.gridN*3), (self.pivotX- self.gridN*3, self.pivotY- self.gridN*3),
                               (self.pivotX- self.gridN*4, self.pivotY- self.gridN*3), (self.pivotX- self.gridN*5, self.pivotY- self.gridN*3), (self.pivotX- self.gridN*6, self.pivotY- self.gridN*3),
                               (self.pivotX- self.gridN*1, self.pivotY+ self.gridN*3), (self.pivotX- self.gridN*2, self.pivotY+ self.gridN*3), (self.pivotX- self.gridN*3, self.pivotY+ self.gridN*3),
                               (self.pivotX- self.gridN*4, self.pivotY+ self.gridN*3), (self.pivotX- self.gridN*5, self.pivotY+ self.gridN*3), (self.pivotX- self.gridN*6, self.pivotY+ self.gridN*3),
                               (self.pivotX, self.pivotY- self.gridN*4), (self.pivotX- self.gridN*1, self.pivotY- self.gridN*4), (self.pivotX- self.gridN*2, self.pivotY- self.gridN*4),
                               (self.pivotX- self.gridN*3, self.pivotY- self.gridN*4), (self.pivotX- self.gridN*4, self.pivotY- self.gridN*4), (self.pivotX- self.gridN*5, self.pivotY- self.gridN*4), (self.pivotX- self.gridN*6, self.pivotY- self.gridN*4),
                               (self.pivotX, self.pivotY+ self.gridN*4), (self.pivotX- self.gridN*1, self.pivotY+ self.gridN*4), (self.pivotX- self.gridN*2, self.pivotY+ self.gridN*4),
                               (self.pivotX- self.gridN*3, self.pivotY+ self.gridN*4), (self.pivotX- self.gridN*4, self.pivotY+ self.gridN*4), (self.pivotX- self.gridN*5, self.pivotY+ self.gridN*4), (self.pivotX- self.gridN*6, self.pivotY+ self.gridN*4),
                               (self.pivotX+ self.gridN, self.pivotY- self.gridN*5), (self.pivotX, self.pivotY- self.gridN*5), (self.pivotX- self.gridN*1, self.pivotY- self.gridN*5),
                               (self.pivotX- self.gridN*2, self.pivotY- self.gridN*5), (self.pivotX- self.gridN*3, self.pivotY- self.gridN*5), (self.pivotX- self.gridN*4, self.pivotY- self.gridN*5), (self.pivotX- self.gridN*5, self.pivotY- self.gridN*5),
                               (self.pivotX+ self.gridN, self.pivotY+ self.gridN*5), (self.pivotX, self.pivotY+ self.gridN*5), (self.pivotX- self.gridN, self.pivotY+ self.gridN*5),
                               (self.pivotX- self.gridN*2, self.pivotY+ self.gridN*5), (self.pivotX- self.gridN*3, self.pivotY+ self.gridN*5), (self.pivotX- self.gridN*4, self.pivotY+ self.gridN*5), (self.pivotX- self.gridN*5, self.pivotY+ self.gridN*5),
                               (self.pivotX+ self.gridN*2, self.pivotY- self.gridN*6), (self.pivotX+ self.gridN, self.pivotY- self.gridN*6), (self.pivotX, self.pivotY- self.gridN*6),
                               (self.pivotX- self.gridN, self.pivotY- self.gridN*6), (self.pivotX- self.gridN*2, self.pivotY- self.gridN*6), (self.pivotX- self.gridN*3, self.pivotY- self.gridN*6), (self.pivotX- self.gridN*4, self.pivotY- self.gridN*6),
                               (self.pivotX+ self.gridN*2, self.pivotY+ self.gridN*6), (self.pivotX+ self.gridN, self.pivotY+ self.gridN*6), (self.pivotX, self.pivotY+ self.gridN*6),
                               (self.pivotX- self.gridN, self.pivotY+ self.gridN*6), (self.pivotX- self.gridN*2, self.pivotY+ self.gridN*6), (self.pivotX- self.gridN*3, self.pivotY+ self.gridN*6), (self.pivotX- self.gridN*4, self.pivotY+ self.gridN*6),
                               (self.pivotX+ self.gridN*2, self.pivotY- self.gridN*7), (self.pivotX+ self.gridN*1, self.pivotY- self.gridN*7), (self.pivotX, self.pivotY- self.gridN*7),
                               (self.pivotX- self.gridN, self.pivotY- self.gridN*7), (self.pivotX- self.gridN*2, self.pivotY- self.gridN*7), (self.pivotX- self.gridN*3, self.pivotY- self.gridN*7),
                               (self.pivotX+ self.gridN*2, self.pivotY+ self.gridN*7), (self.pivotX+ self.gridN*1, self.pivotY+ self.gridN*7), (self.pivotX, self.pivotY+ self.gridN*7),
                               (self.pivotX- self.gridN, self.pivotY+ self.gridN*7), (self.pivotX- self.gridN*2, self.pivotY+ self.gridN*7), (self.pivotX- self.gridN*3, self.pivotY+ self.gridN*7),
                               (self.pivotX+ self.gridN*2, self.pivotY- self.gridN*8), (self.pivotX+ self.gridN*1, self.pivotY- self.gridN*8), (self.pivotX, self.pivotY- self.gridN*8),
                               (self.pivotX- self.gridN, self.pivotY- self.gridN*8), (self.pivotX- self.gridN*2, self.pivotY- self.gridN*8),
                               (self.pivotX+ self.gridN*2, self.pivotY+ self.gridN*8), (self.pivotX+ self.gridN*1, self.pivotY+ self.gridN*8), (self.pivotX, self.pivotY+ self.gridN*8),
                               (self.pivotX- self.gridN, self.pivotY+ self.gridN*8), (self.pivotX- self.gridN*2, self.pivotY+ self.gridN*8),
                               ]
        self._shieldAlocate()
        self.directionY= 1
    
    def _calculate_QotileLaunch(self) -> tuple:
        x= float(self.box.x -self.ship.box.x)
        y= float(self.box.y - self.ship.box.y+10)
        launch_angle= atan2(y, x)

        speedx= cos(launch_angle)
        speedy= sin(launch_angle) * -1
        travelDistance= sqrt(x*x+y*y)

        return (speedx*self.settings.QotileLaunchSpeed, speedy*self.settings.QotileLaunchSpeed, travelDistance)

    def QotileMovement(self):
        if self.directionBox.y > 465:
            self.directionY= -1
        elif self.directionBox.y < 80:
            self.directionY= 1

        if self.attackingStage < 4:
            self.rect.y+= self.settings.QotileSpeed*self.directionY
            self.box.y+= self.settings.QotileSpeed*self.directionY
        else:
            
            self.rect.x-= self.launch_tuple[0]
            self.box.x-= self.launch_tuple[0]
            self.rect.y+= self.launch_tuple[1]
            self.box.y+= self.launch_tuple[1]
            self.traveledDistance+= sqrt(self.launch_tuple[0]*self.launch_tuple[0]+ self.launch_tuple[1]*self.launch_tuple[1])
            if self.launch_tuple[2] <= self.traveledDistance-150:
                self.rect.x, self.rect.y= self.directionBox.x, self.directionBox.y
                self.box.x, self.box.y= self.directionBox.x+90, self.directionBox.y+85
                self.traveledDistance= 0
                self.attackingStage+=1

        self.directionBox.y+= self.settings.QotileSpeed*self.directionY

    def _swirlAnimation(self, screen):
        screen.blit(self.swirl[self.swirlStage], self.rect)

        if self.swirlStage == 2:
            self.swirlStage= 0
        else:
            self.swirlStage+= 1

    def change_color(self, image, new_color):
        arr = pygame.surfarray.pixels3d(image)
        alpha = pygame.surfarray.pixels_alpha(image)
        
        # Create a mask of where the alpha is not zero
        mask = alpha != 0
        # Replace the colors where the mask is True
        arr[mask] = new_color
        
        return image
    
    def _showingQotile(self, screen, color: list):
        self.QotileMovement()
        if self.attackingStage > 2:
            self._swirlAnimation(screen)
        else:
            self.image= self.change_color(self.image, color)
            screen.blit(self.image, self.rect)

    def _shieldGenerate(self, Manager):
        for i in range(101):
            new_shield_cell= QotileShield(Manager, self, i)
            self.QotileShields.add(new_shield_cell)
    def _drawWholeShield(self):
        for shield in self.QotileShields:
            shield.drawShield()
            shield.verticalmovement(self.directionY)

    def _shieldAlocate(self):
        i= 0
        for shield in self.QotileShields:
            shield._updateShieldPos(self.shieldPositions[i])
            i+= 1

    def qotileAi(self, collisionsBulletShield, colisionShip= False):
        match self.attackingStage:
            case 1:
                if self.ship.rect.x > 400:
                    self.agressionLevel+= 0.5
                
                if colisionShip:
                    self.agressionLevel+= 100
                if len(collisionsBulletShield) != 0:
                    self.agressionLevel+= 50
                if self.agressionLevel > 200:
                    self.attackingStage+= 1
                    self.launchtimer= float(time())
            case 2:
                if float(time())- self.launchtimer > 1.5:
                    self.launchtimer= float(time())
                    self.attackingStage+= 1
                    self.time_until_launch= choice((0.1, 1.5, 2, 1))
            case 3:
                if float(time())- self.launchtimer > self.time_until_launch:
                    self.launchtimer= float(time())
                    self.launch_tuple= self._calculate_QotileLaunch()
                    self.attackingStage+= 1
            case 5:
                self.agressionLevel= 0
                self.attackingStage= 1
            
class QotileShield(Sprite):
    def __init__(self, Manager, Qotile, tag) -> None:
        super().__init__()
        self.tag= tag
        self.screen= Manager.screen
        self.settings= Manager.settings
        self.shieldcolor= self.settings.shieldcolor
        self.QotileSpeed= self.settings.QotileSpeed
        self.Qotile= Qotile
        self.rect= pygame.Rect(0,0, self.settings.shieldcellsize, self.settings.shieldcellsize)
        self.rect.x= self.Qotile.rect.x
        self.rect.y= self.Qotile.rect.y
        self.getting_eaten= 0

    def drawShield(self):
        pygame.draw.rect(self.screen, self.shieldcolor, self.rect)

    def _updateShieldPos(self, position: tuple):
        self.rect.x= position[0]
        self.rect.y= position[1]
    
    def verticalmovement(self, directionY):
        self.rect.y+= self.QotileSpeed*directionY