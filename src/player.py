import pygame
from src.boat import Boat
from src.physics import Speed, Pos


class Player(Boat):

    boat_1_image = pygame.image.load("assets/images/boat_friendly.png")
    boat_2_image = pygame.image.load("assets/images/boat_enemy.png")

    def __init__(self, screen: pygame.Surface, pos: Pos, speed: Speed, mass, max_power, boat_image):
        super().__init__(screen, pos, speed, mass, max_power, boat_image)
