import pygame
from math import fabs

class Ship:
    def __init__(self, Manager) -> None:
        self.orientation= 0
        self.flapFrame= 0
        self.settings= Manager.settings
        self.screen= Manager.screen
        self.screen_rect= self.screen.get_rect()
        self.imagecurrent= [pygame.image.load(f'yarSprites\\Player ya{i}.png') for i in ['r', 'r down', 'r left', 'r up', 'r diagonal right', 'r diagonal right down', 'r diagonal left', 'r diagonal left down']]
        self.imagecurrent_flap= [pygame.image.load(f'yarSprites\\Player yar {i}.png') for i in ['flap right', 'flap down', 'flap left', 'flap up', 'diagonal right flap', 'diagonal right down flap', 'diagonal left flap', 'diagonal left down flap']]
        self.death= [pygame.image.load(f'yarSprites\\Yar death anim\\l0_sprite_{i}.png') for i in [1,2,3,4,5]]
        self.rect= self.imagecurrent[0].get_rect()
        self.initial_rect= self.screen_rect.left
        self.box= pygame.Rect(self.rect.x+98, self.rect.y+98, 54, 54)
        self.colisions1= pygame.Rect(self.rect.x+160, self.rect.y+115, 10, 20)
        self.colisions2= pygame.Rect(self.rect.x+80, self.rect.y+115, 10, 20)
        self.colisions3= pygame.Rect(self.rect.x+115, self.rect.y+80, 20, 10)
        self.colisions4= pygame.Rect(self.rect.x+115, self.rect.y+160, 20, 10)
        self.move_right= False
        self.move_left= False
        self.move_up= False
        self.move_down= False
        self.isMoving= False
        self.isAlive= True
        self.isNeutral= False
        self.ZorlonCanonCharged= 0
        self.diagonalcheck= [self.move_down, self.move_left, self.move_right, self.move_up]

    def _blit_ship(self, screen):
        if self.flapFrame> 6:
            self.flapFrame= 0
            screen.blit(self.imagecurrent[self.orientation], self.rect)
            screen.blit(self.imagecurrent_flap[self.orientation], self.rect)
        elif self.flapFrame > 3:
            screen.blit(self.imagecurrent_flap[self.orientation], self.rect)
        else:
            screen.blit(self.imagecurrent[self.orientation], self.rect)
        self.flapFrame+= 1
    def _ship_image_update(self, speed: int, dimensions : tuple):
        self.diagonalcheck= [self.move_down, self.move_left, self.move_right, self.move_up]
        activeR= False
        activeL= False
        nKeyspressed= 0
        for movedir in self.diagonalcheck:
            if movedir:
                nKeyspressed+= 1
        if nKeyspressed > 1:
            usedspeed= self.settings.diagonalshipspeed
        else:
            usedspeed= speed
        #Teleport check
        if dimensions[1]-150 < self.rect.x :
            self.rect.x= dimensions[1]-150
        elif -100 > self.rect.x:
            self.rect.x= -100

        if dimensions[0]-150 < self.rect.y :
            self.rect.y= -100
        elif -100 > self.rect.y:
            self.rect.y= dimensions[0]-150

        #Direction check
        if self.move_left:
            self.orientation= 2
            self.rect.x-= usedspeed
            activeL= True
        if self.move_right:
            self.orientation= 0
            self.rect.x+= usedspeed
            activeR= True
            
        if self.move_up:
            if activeR:
                self.orientation= 4
            elif activeL:
                self.orientation= 6
            else:
                self.orientation= 3
            self.rect.y-= usedspeed

        if self.move_down:
            if activeR:
                self.orientation= 5
            elif activeL:
                self.orientation= 7
            else:
                self.orientation= 1
            self.rect.y+= usedspeed

        if self.move_down or self.move_left or self.move_right or self.move_up:
            self.isMoving= True
        else:
            self.isMoving= False
        #updating colision boxes    
        self.box.x= self.rect.x+98 
        self.box.y= self.rect.y+98
        self.colisions4.x= self.rect.x+115
        self.colisions4.y= self.rect.y+160
        self.colisions1.x= self.rect.x+160
        self.colisions1.y= self.rect.y+115
        self.colisions3.x= self.rect.x+115
        self.colisions3.y= self.rect.y+80
        self.colisions2.x= self.rect.x+80
        self.colisions2.y= self.rect.y+115
    
    def _play_Ship_Death(self, screen, anim_counter):
        match anim_counter:
            case -4:
                if self.orientation != 0:
                    self.orientation= 0
                screen.blit(self.imagecurrent[self.orientation], self.rect)
            case -3:
                screen.blit(self.imagecurrent[self.orientation+1], self.rect)
            case -2:
                screen.blit(self.imagecurrent[self.orientation+2], self.rect)
            case -1:
                screen.blit(self.imagecurrent[self.orientation+3], self.rect)
            case _:
                try:
                    screen.blit(self.death[anim_counter], self.rect)
                except IndexError:
                    pass