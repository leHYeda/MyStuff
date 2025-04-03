import pygame

class SoundManager:
    def __init__(self) -> None:
        self.mixer= pygame.mixer
        self.mixer.init()
    
    def _ambient_sound(self):
        pass
    