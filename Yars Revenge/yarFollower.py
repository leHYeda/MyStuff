import pygame

class yarFollower():
    def __init__(self, Manager):
        self.screen_rect= Manager.screen.get_rect()
        self.initial_rect= self.screen_rect
        self.rect= pygame.Rect(0,0, 36, 6)
        self.rect.centery= self.initial_rect.centery
        self.rect.right= self.initial_rect.right+50
        self.settings= Manager.settings
        self.screen= Manager.screen
        self.ship= Manager.ship
        self.playerBox= self.ship.box

    def followPlayer(self):
        if self.playerBox.x < self.rect.x:
            self.rect.x-= self.settings.followerSpeed
        elif self.playerBox.x > self.rect.x:
            self.rect.x+= self.settings.followerSpeed

        if self.playerBox.y < self.rect.y:
            self.rect.y-= self.settings.followerSpeed
        elif self.playerBox.y > self.rect.y:
            self.rect.y+= self.settings.followerSpeed
    def draw_follower(self, color: list):
        pygame.draw.rect(self.screen, color, self.rect)
    