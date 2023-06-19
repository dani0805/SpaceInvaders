# player spaceship entity

import pygame

from entities.entity import Entity
from entities.laser import Laser


class Ship(Entity):

    def __init__(self, game):
        super().__init__(game, (400, 500))
        self.image = pygame.image.load('images/ship.png')
        self.orginal_image = self.image
        # draw a dark blue triangle as the ship in self.image (the ship is 32x32 pixels)
        # self.image = pygame.Surface((32, 32))
        # self.image.fill((0, 0, 0))
        # pygame.draw.polygon(self.image, (0, 0, 128), ((0, 32), (16, 0), (32, 32)))
        self.moving = 0
        self.speed = 5
        self.charging = 0
        self.charge_speed = 20

    def update(self, events):
        # move the ship left or right if the keys are pressed, continue moving until the key is released
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.moving = - self.speed
                elif event.key == pygame.K_RIGHT:
                    self.moving = self.speed
                elif event.key == pygame.K_SPACE and self.charging == 0:
                    self.game.state.add_entity(Laser(self.game, (self.position[0] + 14, self.position[1] - 32), -5))
                    self.charging = self.charge_speed


            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.moving = 0

        if self.charging > 0:
            self.charging -= 1

        self.position = (self.position[0] + self.moving, self.position[1])

        if self.moving < 0:
            # sqeeze the ship and tilt it to the left
            self.image = pygame.transform.scale(self.orginal_image, (24, 32))
            self.image = pygame.transform.rotate(self.image, 5)
            # make the ship darker
            self.image.fill((30, 30, 30), special_flags=pygame.BLEND_SUB)
        elif self.moving > 0:
            # sqeeze the ship and tilt it to the right
            self.image = pygame.transform.scale(self.orginal_image, (24, 32))
            self.image = pygame.transform.rotate(self.image, -5)
            # make the ship lighter
            self.image.fill((30, 30, 30), special_flags=pygame.BLEND_ADD)
        else:
            # reset the ship image
            self.image = self.orginal_image



        # keep the ship inside the screen
        if self.position[0] < 0:
            self.position = (0, self.position[1])
        elif self.position[0] > 768:
            self.position = (768, self.position[1])



