# alien class implementation

import pygame

from entities.entity import Entity


class Alien(Entity):

    def __init__(self, game, type, position, strategy):
        super().__init__(game, position)
        self.type = type
        self.strategy = strategy
        self.image = pygame.image.load('images/alien_' + str(type) + '.png')
        self.attacking = 0

        # draw a dark green triangle as the alien in self.image
        # self.image = pygame.Surface((32, 32))
        # self.image.fill((0, 0, 0))
        # pygame.draw.polygon(self.image, (0, 128, 0), ((0, 0), (16, 32), (32, 0)))

    def update(self, events):
        self.strategy.update(self, events)
