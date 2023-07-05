from src.game import Game
from sys import argv


def main(window_width: int = 1080, window_height: int = 720):
    """Start the game
    """
    game = Game(window_width, window_height)
    game.run()


if __name__ == '__main__':

    if len(argv) == 3:
        main(int(argv[1]), int(argv[2]))
    else:
        main()
