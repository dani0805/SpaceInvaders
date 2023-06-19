import pygame
import sys

from states.start import Start
from states.play import Play
from states.gameover import GameOver


class Game:

    def __init__(self, name):
        self.name = name
        # make window resizable

        self.screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        pygame.display.set_caption(name)
        self.clock = pygame.time.Clock()
        self.state = Start(self)
        self.scaling_factor = 1
        self.origin = (0, 0)

    def run(self):
        while True:
            events = pygame.event.get()
            for event in events:
                # handle resize drag
                if event.type == pygame.VIDEORESIZE:
                    self.resolution = event.size
                # handle quit
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.state = self.state.update(events)
            self.state.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

    @property
    def resolution(self):
        return self.screen.get_size()

    @resolution.setter
    def resolution(self, value):
        self.screen = pygame.display.set_mode(value, pygame.RESIZABLE)
        self.scaling_factor = min(value[0] / 800, value[1] / 600)
        self.origin = (value[0] / 2 - 400 * self.scaling_factor,
                       value[1] / 2 - 300 * self.scaling_factor)

    def new_state(self, state_name):
        if state_name == "gameover":
            return GameOver(self)
        elif state_name == "play":
            return Play(self)
        elif state_name == "start":
            return Start(self)


