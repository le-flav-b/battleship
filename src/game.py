import time

import pygame
from src import terrainGen


class Game:
    """General class for the game
    """

    def __init__(self):
        """Create the pygame window and initialize all the elements of the game
        """

        self.screen_size = (1080, 720)
        self.sealevel = 145

        # calcul du temps de création de la carte
        t_debut = time.time()
        # création de la carte (heightmap)
        self.map_data = terrainGen.GenerateMap(self.screen_size)
        # création de l'image associée à la carte
        self.map_image = pygame.surfarray.make_surface(
            terrainGen.ColorMap(self.map_data)
            .get_color_map_array(self.sealevel))
        t_fin = time.time()

        print("Map générée en " + str(int((t_fin-t_debut)*1000)) + " ms")

        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_icon(pygame.image.load('assets/images/icon.png'))
        pygame.display.set_caption('Battleship')

        self.running = False

    def run(self):
        """Run the game
        """

        self.running = True

        while self.running:

            # afficher qqchose à l'écran
            self.screen.blit(self.map_image, (0, 0))

            # mettre à jour l'écran
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

        self.close()

    def close(self):
        """Close the game
        """
        pygame.quit()
