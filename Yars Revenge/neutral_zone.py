import pygame
from pathlib import Path
from random import randint

class NeutralZ:
    def __init__(self, Manager) -> None:
        self.screen= Manager.screen
        self.settings= Manager.settings
        self.font= Manager.font
        self.zone= pygame.Rect(350, 0, 150, 800)
        self.path= Path("code.txt")
        self.lines= self._lineSplit()
        self.lines2= self._lineSplit()

    def _lineSplit(self):
        contents= self.path.read_text()
        contents= contents.rstrip()
        return contents.splitlines()
    
    def text_generator(self, text_to_print, color, position: tuple):
        if type(text_to_print) == str:
            texto= self.font.render(text_to_print , True, color, self.settings.bg_color)
            self.screen.blit(texto, position)

        elif type(text_to_print) == int:
            text_to_print= str(text_to_print)
            texto= self.font.render(text_to_print , True, color, self.settings.bg_color)
            self.screen.blit(texto, position)
            text_to_print= int(text_to_print)

    def _code_draw(self):
        i= 0
        for lines in self.lines:
            self.text_generator(lines, (randint(25, 250), randint(25, 250), randint(25, 250)), (350, i))
            if len(lines) <= 45:
                self.text_generator(lines, (randint(25, 250), randint(25, 250), randint(25, 250)), (420, i))
            i+=2
        self.lines.insert(0, self.lines[-1])
        self.lines.insert(1, self.lines[-2])
        del(self.lines[-1])
        del(self.lines[-2])
        
    def _code_draw_inverse(self):
        i= 0
        for lines in self.lines2:
            self.text_generator(lines, (randint(25, 250), randint(25, 250), randint(25, 250)), (350, i))
            if len(lines) <= 45:
                self.text_generator(lines, (randint(25, 250), randint(25, 250), randint(25, 250)), (420, i))
            i+=2
        self.lines2.insert(-1, self.lines2[0])
        self.lines2.insert(-2, self.lines2[1])
        del(self.lines2[0])
        del(self.lines2[1])
    def test_draw(self):
        pygame.draw.rect(self.screen, (0,200,200), self.zone)