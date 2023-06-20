# normal slow descent strategy, alien moves right for a while, then down and then left for a while and then down again
# rinse and repeat

from strategies.strategy import Strategy



class FastDescent(Strategy):

    def __init__(self, game):
        super().__init__(game)
        self._direction = (0, 1)

    def update(self, entity, events):
        speed = 0.75 + entity.game.state.level / 4
        entity.position = (entity.position[0] + self._direction[0] * speed, entity.position[1] + self._direction[1] * speed)
        # if the alien is out of the screen, remove it
        if entity.position[1] > 600:
            entity.game.state.remove_entity(entity)

