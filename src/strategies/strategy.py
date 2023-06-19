# abstract class for entities strategy

from abc import ABC, abstractmethod


class Strategy(ABC):

    def __init__(self, game):
        self.game = game

    @abstractmethod
    def update(self, entity, events):
        raise NotImplementedError()