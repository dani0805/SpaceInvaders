# play game state

import sys
import pygame
from states.game_state import GameState
from entities.alien import Alien
from strategies.slow import NormalSlowDescent
from entities.ship import Ship


class Play(GameState):

    def __init__(self, game):
        super().__init__(game)
        self._entities = []
        self.lives = 3
        self.score = 0
        self._level = 5
        self.starting = 120
        # create 3 rows of 10 aliens each
        # the aliens are 32x32 pixels and start at the top left corner, evenly spaced so that they occupy
        # the whole screen width except for the last 60 pixels on the right
        v_offset = 32
        h_offset = (800 - 60 - 32 * 10) / 9
        for row in range(3):
            for column in range(10):
                self._entities.append(Alien(
                    self.game,
                    (row + column) % 2,
                    (column * (32 + h_offset), row * (32 + v_offset)),
                    NormalSlowDescent(self.game)
                ))

        # create the spaceship
        self.ship = Ship(self.game)
        self._entities.append(self.ship)
        self.spare_ship_image = self.ship.image

    def update(self, events) -> "GameState":
        if self.starting > 0:
            self.starting -= 1
            return self
        for entity in self._entities:
            entity.update(events)

        # loop through all the entities and check for collisions
        for entity in self._entities:
            if isinstance(entity, Alien):
                for other_entity in self._entities:
                    if isinstance(other_entity, Alien):
                        continue
                    if entity.collides(other_entity):
                        if isinstance(other_entity, Ship):
                            return self.ship_destroyed()
                        self._entities.remove(entity)
                        self._entities.remove(other_entity)
                        self.score += 1 * self.level * (1 + entity.attacking)
                        break
            elif isinstance(entity, Ship):
                for other_entity in self._entities:
                    if other_entity is not entity and entity.collides(other_entity):
                        return self.ship_destroyed()
        # if there are no more aliens, go to the next level
        if len([entity for entity in self._entities if isinstance(entity, Alien)]) == 0:
            new_state = self.game.new_state("play")
            new_state.level = self.level + 1
            new_state.score = self.score
            return new_state
        return self

    def ship_destroyed(self):
        if self.lives > 1:
            self.lives -= 1
            new_state = self.game.new_state("play")
            new_state.lives = self.lives
            new_state.score = self.score
            new_state.level = self.level
            return new_state
        else:
            new_state = self.game.new_state("gameover")
            new_state.score = self.score
            return new_state

    def draw(self, screen):
        # draw the background
        screen.fill((0, 0, 0))
        # draw lives - 1 ships in the bottom left corner
        for i in range(self.lives - 1):
            screen.blit(self.spare_ship_image, (i * 32, self.game.resolution[1] - 32))

        # draw the title
        for entity in self._entities:
            entity.draw(screen)
        # draw the score in the bottom right corner
        font = pygame.font.SysFont('Arial', 30)
        score = font.render(f"SCORE: {self.score}", True, (255, 255, 255))
        score_rect = score.get_rect()
        score_rect.bottomright = self.game.resolution[0] - 10, self.game.resolution[1] - 10
        screen.blit(score, score_rect)

        if self.starting > 0:
            font = pygame.font.SysFont('Arial', 30)
            score = font.render("Level " + str(self.level - 4), True, (255, 255, 255))
            score_rect = score.get_rect()
            score_rect.center = self.game.resolution[0] / 2, self.game.resolution[1] / 2
            screen.blit(score, score_rect)

    def add_entity(self, entity):
        self._entities.append(entity)

    def remove_entity(self, entity):
        self._entities.remove(entity)

    @property
    def entities(self):
        return self._entities

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = value

