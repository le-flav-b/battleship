import pygame
from src.boat import Boat
from src.physics import Speed, Pos


class Player(Boat):

    boat_1_image = pygame.image.load("assets/images/boat_enemy.png")
    boat_2_image = pygame.image.load("assets/images/boat_friendly.png")

    def __init__(self, pos: Pos, speed: Speed, mass, max_power, image):
        super().__init__(pos, speed, mass, max_power)
        self.image = image
