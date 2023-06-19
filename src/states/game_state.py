# abstract class for the game state

from abc import ABC, abstractmethod


class GameState(ABC):

    def __init__(self, game):
        self.game = game

    @abstractmethod
    def update(self, events) -> "GameState":
        raise NotImplementedError()

    @abstractmethod
    def draw(self, screen):
        raise NotImplementedError()


