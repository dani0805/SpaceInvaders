# normal slow descent strategy, alien moves right for a while, then down and then left for a while and then down again
# rinse and repeat

import pygame
import random

from strategies.strategy import Strategy
from strategies.fast import FastDescent
from entities.laser import Laser
from entities.alien import Alien


class NormalSlowDescent(Strategy):

    def __init__(self, game):
        super().__init__(game)
        self._direction = 1
        self._counter = 0

    def update(self, entity, events):
        speed = 0.75 + entity.game.state.level / 4
        self._counter += 1
        if self._counter == 60 // speed:
            self._direction *= -1
            self._counter = 0
            entity.position = (entity.position[0], entity.position[1] + speed)
        else:
            entity.position = (entity.position[0] + self._direction * speed, entity.position[1])

        # check if the alien has similar x coordinate with another alien and has lower y coordinate than that alien
        # if so, do not fire a laser beam
        for other_entity in self.game.state.entities:
            if other_entity is entity:
                continue
            if isinstance(other_entity, Laser):
                continue
            if isinstance(other_entity, Alien):
                if other_entity.position[0] < entity.position[0] + 32 \
                        and other_entity.position[0] + 32 > entity.position[0] \
                        and other_entity.position[1] > entity.position[1]:
                    return

        # otherwise fire a laser beam at random
        frequency = 1000 - self.game.state.level * 50
        if random.randint(0, frequency) == 0:
            self.game.state.add_entity(Laser(self.game, (entity.position[0] + 16, entity.position[1] + 32), 5))

        # alternatively change the strategy to fast descent
        if random.randint(0, frequency) == 0:
            entity.strategy = FastDescent(self.game)
            # aim at the player
            entity.strategy._direction = (self.game.state.ship.position[0] - entity.position[0], self.game.state.ship.position[1] - entity.position[1])
            # normalize the direction
            length = (entity.strategy._direction[0] ** 2 + entity.strategy._direction[1] ** 2) ** 0.5
            entity.strategy._direction = (entity.strategy._direction[0] / length, entity.strategy._direction[1] / length)
            entity.attacking = 1