import pygame


class Game:
    """General class for the game
    """

    def __init__(self):
        """Create the pygame window and initialize all the elements of the game
        """

        pygame.init()
        pygame.display.set_mode((1080, 720))
        pygame.display.set_icon(pygame.image.load('assets/images/icon.png'))
        pygame.display.set_caption('Battleship')

        self.running = False

    def run(self):
        """Run the game
        """

        self.running = True

        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
        
        self.close()

    def close(self):
        """Close the game
        """
        pygame.quit()
