import sys
from random import randint
import pygame
from pygame.locals import*
from settings import Settings
from ship import Ship
from Qotile import Qotile
from bullet import Bullet
from bullet import Cannon
from yarFollower import yarFollower
from neutral_zone import NeutralZ
from time import time

class GameManager:
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        pygame.display.set_icon(pygame.image.load("yarSprites\\yars revenge icon.jpg"))
        pygame.display.set_caption("Yar's revenge Scuffed Version")
        self.font= pygame.font.SysFont(None, 5)
        self.clock= pygame.time.Clock()
        self.settings= Settings()
        self.settings.findingSpeed()
        self.settings.findingSpeedShip()
        self.screen= pygame.display.set_mode((self.settings.screenwidth, self.settings.screenheigh))
        self.ship= Ship(self)
        self.Qotile= Qotile(self)
        self.bullets= pygame.sprite.Group()
        self.cannon= pygame.sprite.Group()
        self.yarFollower= yarFollower(self)
        self.neutral= NeutralZ(self)
        self.colorChange= [0, 0, 200]
        self.anim_counter= -4
        self.lives= 3
        self.points= 0
        pygame.mouse.set_visible(False)

    def huechange(self):
        if self.Qotile.attackingStage > 3:
            self.colorChange= list(self.settings.shieldcolor)
        
        elif self.Qotile.attackingStage == 2:

            if self.colorChange[2] < 35:
                self.colorChange[2]+= randint(0,3)
            else:
                self.colorChange[2]= 5

            if self.colorChange[1] < 150:
                self.colorChange[1]+= randint(0,5)
            else:
                self.colorChange[1]= 25

            if self.colorChange[0] < 200:
                self.colorChange[0]+= randint(0,5)
            else:
                self.colorChange[0]= 25

        else:
            if self.colorChange[2] < 200:
                self.colorChange[2]+= randint(0,5)
            else:
                self.colorChange[2]= 25
            if self.colorChange[1] < 200:
                self.colorChange[1]+= randint(0,5)
            else:
                self.colorChange[1]= 25
            if self.colorChange[0] < 35:
                self.colorChange[0]+= randint(0,3)
            else:
                self.colorChange[0]= 5

    def _screen_update(self):
        global start_time2
        self.screen.fill(self.settings.bg_color)

        #pygame.draw.rect(self.screen, (0, 200, 0), self.Qotile.box)
        #pygame.draw.rect(self.screen, (0, 200, 0), self.ship.box)
        #pygame.draw.rect(self.screen, (0, 0, 200), self.ship.colisions1)
        #pygame.draw.rect(self.screen, (0, 0, 200), self.ship.colisions2)
        #pygame.draw.rect(self.screen, (0, 0, 200), self.ship.colisions3)
        #pygame.draw.rect(self.screen, (0, 0, 200), self.ship.colisions4)
        #self.neutral.test_draw()
        self.neutral._code_draw()
        self.neutral._code_draw_inverse()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for cannon in self.cannon.sprites():
            cannon.draw_cannon()
        
        if self.ship.isAlive == False:
            if float(time())- start_time2 > 0.15:
                start_time2= float(time())
                self.anim_counter+= 1
            self.ship._play_Ship_Death(self.screen, self.anim_counter)
        else:
            self.ship._blit_ship(self.screen)
        self.yarFollower.draw_follower(self.colorChange)
        self.huechange()
        if self.ship.isAlive or self.Qotile.attackingStage != 4:
            self.Qotile._showingQotile(self.screen, self.colorChange)
        self.Qotile._drawWholeShield()
        pygame.display.flip()
    
    def _check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    case pygame.K_F4:
                        pygame.display.toggle_fullscreen()
                        pygame.display.set_icon(pygame.image.load("yarSprites\\yars revenge icon.jpg"))
                    case pygame.K_RIGHT | pygame.K_d:
                        self.ship.move_right= True
                    case pygame.K_LEFT | pygame.K_a:
                        self.ship.move_left= True
                    case pygame.K_DOWN | pygame.K_s:
                        self.ship.move_down= True
                    case pygame.K_UP | pygame.K_w:
                        self.ship.move_up= True
                    case pygame.K_SPACE:
                        if self.ship.ZorlonCanonCharged < 2 and self.ship.isNeutral == False:
                            self._bullet_fire()
                        else:
                            self._cannon_fire()

            elif event.type == pygame.KEYUP:
                match event.key:
                    case pygame.K_RIGHT | pygame.K_d:
                        self.ship.move_right= False
                    case pygame.K_LEFT | pygame.K_a:
                        self.ship.move_left= False
                    case pygame.K_DOWN | pygame.K_s:
                        self.ship.move_down= False
                    case pygame.K_UP | pygame.K_w:
                        self.ship.move_up= False
    
    def _basic_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_F4:
                    pygame.display.toggle_fullscreen()
                    pygame.display.set_icon(pygame.image.load("yarSprites\\yars revenge icon.jpg"))
    def _bullet_fire(self):
        global start_time
        end_time= float(time())
        if len(self.bullets) < self.settings.maximumbullets and end_time-start_time > 0.5:
            start_time= float(time())
            new_bullet= Bullet(self)
            self.bullets.add(new_bullet)
    
    def _cannon_add(self):
        if self.ship.ZorlonCanonCharged >= 2 and len(self.cannon) == 0:
            cannon_shot= Cannon(self)
            self.cannon.add(cannon_shot)
    def _cannon_fire(self):
        for cannon in self.cannon.copy():
            cannon.cannonFollowState= False
        self.ship.ZorlonCanonCharged= 0
    def _run_game(self):
        global start_time2
        while True:
            if self.ship.isAlive == True:
                self._check_event()
            else:
                break
            collisionsBulletShield= pygame.sprite.groupcollide(self.bullets, self.Qotile.QotileShields, True, True)
            collisionsCannonShield= pygame.sprite.groupcollide(self.cannon, self.Qotile.QotileShields, True, True)

            for shield in self.Qotile.QotileShields:
                if pygame.Rect.colliderect(shield.rect, self.ship.box):
                    if pygame.Rect.colliderect(shield.rect, self.ship.colisions1):
                        self.ship.rect.x-= self.settings.EatingOffset
                    if pygame.Rect.colliderect(shield.rect, self.ship.colisions2):
                        self.ship.rect.x+= self.settings.EatingOffset
                    if pygame.Rect.colliderect(shield.rect, self.ship.colisions3):
                        self.ship.rect.y+= self.settings.EatingOffset
                    if pygame.Rect.colliderect(shield.rect, self.ship.colisions4):
                        self.ship.rect.y-= self.settings.EatingOffset
                        
                    if self.ship.isMoving and self.ship.isAlive:
                        shield.getting_eaten+=1
                        if shield.getting_eaten > 15:
                            self.Qotile.QotileShields.remove(shield)
                            self.points+= 169
                            self.ship.ZorlonCanonCharged+= 1
                            break
                                
            for bullet in self.bullets.copy():
                if bullet.rect.x > self.settings.screenwidth or bullet.rect.y > self.settings.screenheigh:
                    self.bullets.remove(bullet)
                elif bullet.rect.x < 0 or bullet.rect.y < 0:
                    self.bullets.remove(bullet)

            self.ship._ship_image_update(self.settings.speed, (self.settings.screenheigh, self.settings.screenwidth))
            self.bullets.update(self.ship.orientation)
            
            for cannon in self.cannon.copy():
                if cannon.rect.x > self.settings.screenwidth:
                    self.cannon.remove(cannon)
                if pygame.Rect.colliderect(cannon.rect, self.Qotile.box): #Winning condition
                    self.cannon.remove(cannon)
                    match self.Qotile.attackingStage:
                        case 1:
                            self.points+= 1000
                        case 2 | 3:
                            self.points+= 2000
                        case 4:
                            self.points+= 6000
                            self.lives+= 1

                if pygame.Rect.colliderect(cannon.rect, self.ship.box) and self.ship.isNeutral == False:
                    self.ship.isAlive= False
                    self.lives-= 1
                    self.cannon.remove(cannon)
            collision= False
            if pygame.Rect.colliderect(self.Qotile.box, self.ship.box) and self.Qotile.attackingStage == 1:
                self.ship.ZorlonCanonCharged= 2
                collision= True
            if pygame.Rect.colliderect(self.Qotile.box, self.ship.box) and self.Qotile.attackingStage == 4:
                self.ship.isAlive= False
                self.lives-= 1
            if pygame.Rect.colliderect(self.yarFollower.rect, self.ship.box):
                self.ship.isAlive= False
                self.lives-= 1
            if pygame.Rect.colliderect(self.neutral.zone, self.ship.box):
                self.ship.isNeutral= True
            else:
                self.ship.isNeutral= False

            end_time= float(time())
            if end_time-start_time2 > 0.06:
                start_time2= float(time())
                self.yarFollower.followPlayer()

            if self.ship.ZorlonCanonCharged >= 2:
                self._cannon_add()
            self.Qotile.qotileAi(collisionsBulletShield, collision)
            if len(collisionsCannonShield) != 0:
                self.points+= 69
            self._screen_update()
            self.clock.tick(60)
            
    def text_generator(self, text_to_print, color, position: tuple):
        if type(text_to_print) == str:
            texto= self.font.render(text_to_print , True, color, self.settings.bg_color)
            self.screen.blit(texto, position)

        elif type(text_to_print) == int:
            text_to_print= str(text_to_print)
            texto= self.font.render(text_to_print , True, color, self.settings.bg_color)
            self.screen.blit(texto, position)
            text_to_print= int(text_to_print)

    def _basic_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.font= pygame.font.SysFont(None, 64)
        self.text_generator(self.points, (165, 0, 240), (600, 100))
        self.text_generator(self.lives, (165, 0, 240), (600, 250))
        pygame.display.flip()
####################
if __name__ == "__main__":
    start_time= float(time())
    start_time2= start_time
    runner= GameManager()
    while True:
        runner._run_game()
        runner._basic_events()
        if runner.anim_counter < 9:
            start_time= float(time())
            runner._screen_update()
        else:
            runner._basic_screen()
            if float(time())-start_time > 2.5:
                runner.ship.__init__(runner)
                if runner.lives == 0:
                    runner.lives= 3
                    runner.points= 0
                runner.anim_counter= -4
                runner.yarFollower.__init__(runner)
                runner.Qotile.__init__(runner)

        runner.clock.tick(30)