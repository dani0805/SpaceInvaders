# Start state class
import sys
import pygame
from states.game_state import GameState



class Start(GameState):

    def update(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # switch to the play state
                return self.game.new_state("play")
        return self

    def draw(self, screen):
        # draw the background
        screen.fill((0, 0, 0))
        # draw the title
        font = pygame.font.SysFont('Arial', 30)
        title = font.render('Space Invaders', True, (255, 255, 255))
        title_rect = title.get_rect()
        title_rect.center = self.game.resolution[0] / 2, self.game.resolution[1] / 2
        screen.blit(title, title_rect)
        # draw the instructions
        instructions = font.render('Click to start', True, (255, 255, 255))
        instructions_rect = instructions.get_rect()
        instructions_rect.center = self.game.resolution[0] / 2, self.game.resolution[1] / 2 + 50
        screen.blit(instructions, instructions_rect)




