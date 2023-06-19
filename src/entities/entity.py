# abstract class for entities

from abc import ABC, abstractmethod

import pygame


class Entity(ABC):

    def __init__(self, game, position):
        self.position = position
        self.image = None
        self.game = game

    @abstractmethod
    def update(self, events):
        raise NotImplementedError()

    def draw(self, screen):
        scaled_position = (self.position[0] * self.game.scaling_factor + self.game.origin[0],
                           self.position[1] * self.game.scaling_factor + self.game.origin[1])
        scaled_size = (self.image.get_size()[0] * self.game.scaling_factor,
                       self.image.get_size()[1] * self.game.scaling_factor)
        scaled_image = pygame.transform.scale(self.image, scaled_size)
        screen.blit(scaled_image, scaled_position)

    def collides(self, other):
        return self.position[0] < other.position[0] + other.image.get_size()[0] and \
               self.position[0] + self.image.get_size()[0] > other.position[0] and \
               self.position[1] < other.position[1] + other.image.get_size()[1] and \
               self.position[1] + self.image.get_size()[1] > other.position[1]

