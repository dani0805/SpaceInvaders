# Game Over State

import pygame
import os

from states.game_state import GameState


class GameOver(GameState):

    def __init__(self, game):
        super().__init__(game)
        self._score = 0
        self.index = 0
        # load the high scores
        self.high_scores = []
        # create the high scores file if it doesn't exist
        if not os.path.exists("high_scores.txt"):
            with open("high_scores.txt", "w") as file:
                pass
        with open("high_scores.txt", "r") as file:
            for line in file:
                score = line.split()
                if len(score) < 2:
                    score = ("AAA", "0")
                self.high_scores.append(score)

    def update(self, events):
        # update the name of the player for the high score
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # switch to the play state
                    return self.game.new_state("play")
                elif event.key == pygame.K_BACKSPACE and self.index > 0:
                    self.high_scores[self.index][0] = self.high_scores[self.index][0][:-1]
                elif len(self.high_scores[self.index][0]) < 3 and self.index > 0:
                    self.high_scores[self.index][0] += event.unicode
        # save the high scores
        with open("high_scores.txt", "w") as file:

            for score in self.high_scores:
                file.write(" ".join(score) + "\n")
        return self

    def draw(self, screen):
        # draw the background
        screen.fill((0, 0, 0))
        # draw the title
        font = pygame.font.SysFont("Arial", 72)
        text = font.render("Game Over", True, (255, 255, 255))
        screen.blit(text, (200, 50))
        font = pygame.font.SysFont("Arial", 36)
        text = font.render("Press ESC to restart", True, (255, 255, 255))
        screen.blit(text, (200, 150))
        # draw the high scores in mono spaced font
        font = pygame.font.SysFont("Courier", 36)
        for i, score in enumerate(self.high_scores):
            # fill the name with spaces to make it 3 characters long
            name = score[0] + " " * (3 - len(score[0]))
            # highlight the current score using a different color
            if i == self.index:
                text = font.render(name + " " + score[1], True, (255, 0, 255))
            else:
                text = font.render(score[0] + " " + score[1], True, (255, 255, 255))
            screen.blit(text, (200, 200 + i * 50))


    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value
        # add the current score to the high scores
        self.high_scores.append(["", str(self._score)])
        # sort the high scores
        self.high_scores.sort(key=lambda x: int(x[1]), reverse=True)
        # find the index of the current score (empty name and score matching the current score)
        self.index = [i for i, score in enumerate(self.high_scores) if score[0] == "" and int(score[1]) == self._score][0]
        if self.index > 7:
            self.index = -1
        self.high_scores = self.high_scores[:8]