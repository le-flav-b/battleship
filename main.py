from src.game import Game
from sys import argv  ## will be removed


def main(window_width: int = 1080, window_height: int = 720) -> None:
    """Start the game
    """
    game = Game(window_width, window_height)
    game.run()


if __name__ == '__main__':

    ## To see the game responsiveness, will be removed
    if len(argv) == 2:
        main(int(argv[1]), int(argv[1]) // 3 * 2)
    elif len(argv) == 3:
        main(int(argv[1]), int(argv[2]))
    else:
        main()
