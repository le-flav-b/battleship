import math
import pygame
from pygame import Surface

from src.physics import Dot, Pos, Speed, Force


class Boat(pygame.sprite.Sprite):

    boat_bot_image = pygame.image.load("assets/images/boat_bot.png")

    def __init__(self, pos: Pos, speed: Speed, mass, max_power):
        """création du bateau, orientation en radians"""
        super().__init__()
        self.dot = Dot(pos, speed, mass)
        self.orientation = self.dot.speed.get_orientation()
        if self.orientation is None:
            self.orientation = 0
        self.engine_power = 0
        self.max_power = max_power
        self.coeff_friction = 5

        self.size_image = (48, 16)
        self.base_image = pygame.transform.scale(Boat.boat_bot_image, self.size_image)
        self.image = self.base_image
        self.rect = self.image.get_rect()

    def rotate(self, angle):
        """lorsque le bateau tourne, il conserve sa vitesse
        le bateau tourne moins vite lorsqu'il est à l'arrêt"""
        speed_norm = self.dot.speed.get_norm()
        if speed_norm != 0:
            self.orientation += angle
        else:
            self.orientation += 0.4*angle
        self.dot.speed.x = math.cos(self.orientation) * speed_norm
        self.dot.speed.y = math.sin(self.orientation) + speed_norm

    def set_engine_power(self, power):
        """régulateur sur la puissance afin de ne pas dépasser le max"""
        if power <= -self.max_power:
            self.engine_power = -self.max_power
        elif power <= self.max_power:
            self.engine_power = power
        else:
            self.engine_power = self.max_power

    def run(self, time_step):
        """calcul des forces en présence et application de la seconde loi de Newton"""
        self.orientation = self.dot.speed.get_orientation()
        engine_force = Force(self.engine_power * math.cos(self.orientation),
                             self.engine_power * math.sin(self.orientation))
        speed_norm = self.dot.speed.get_norm()
        friction_force = Force(self.coeff_friction * speed_norm * math.cos(self.orientation),
                               self.coeff_friction * speed_norm * math.sin(self.orientation))
        resultant = engine_force + friction_force
        self.dot.run(resultant, time_step)

    def display_boat(self, screen: Surface):
        self.image = pygame.transform.rotate(self.base_image, self.orientation * 180 / math.pi)
        self.rect = self.image.get_rect()
        self.rect.center = (self.dot.pos.x, self.dot.pos.y)
        screen.blit(self.image, self.rect)