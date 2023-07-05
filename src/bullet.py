import math
import pygame

from src.boat import Boat
from src.physics import Dot, Force, Pos, Speed


class Bullet:

    def __init__(self, shooter_boat: Boat, pos: Pos, speed: Speed):
        self.shooter_boat = shooter_boat
        self.dot = Dot(pos, speed, 0.1)

    def run(self, time_step):
        self.dot.run(Force(0, 0), time_step)
