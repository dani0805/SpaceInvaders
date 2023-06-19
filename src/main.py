# main function of PyGame game space invaders
# the game follows a State pattern to manage the different states of the game
# the game is composed of 3 states: start, play and game over
# the main function is responsible for managing the main loop and
# switching between the different states
import pygame

from game import Game


def main(name):
    pygame.init()
    game = Game(name)
    game.run()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
