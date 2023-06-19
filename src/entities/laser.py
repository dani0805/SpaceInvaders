# entity class for laser beam

import pygame

from entities.entity import Entity


class Laser(Entity):

    def __init__(self, game, position, speed):
        super().__init__(game, position)
        #self.image = pygame.image.load('images/laser.png')
        # draw a red line as the laser beam in self.image
        self.image = pygame.Surface((3, 32))
        self.image.fill((128, 0, 0))
        self.speed = speed

    def update(self, events):
        self.position = (self.position[0], self.position[1] + self.speed)
        if self.position[1] < 0 or self.position[1] > 600:
            self.game.state.remove_entity(self)
