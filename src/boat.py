import math
import pygame

from src.physics import Dot, Pos, Speed, Force


class Boat(pygame.sprite.Sprite):
    boat_bot_image = pygame.image.load("assets/images/boat_bot.png")

    def __init__(self, pos: Pos, speed: Speed, mass, max_power=1000, boat_image=boat_bot_image):
        """création du bateau, orientation en radians"""
        super().__init__()

        # boat's mechanics constants
        self.engine_power = 0
        self.max_power = max_power
        self.coeff_water_friction = 5
        self.coeff_sand_friction = 1000
        self.coeff_swivel = 1e-3

        # boat's mechanics related
        self.dot = Dot(pos, speed, mass)
        self.orientation = self.dot.speed.get_orientation()
        if self.orientation is None:
            self.orientation = 0

        # pygame's related
        self.size_image = (48, 16)
        self.base_image = pygame.transform.scale(boat_image, self.size_image)
        self.image = self.base_image
        self.rect = self.image.get_rect()
        self.rect.center = (self.dot.pos.x, self.dot.pos.y)

        # game's mechanics related
        self.max_health = 100
        self.health = 60
        self.bullets_damage = 5

    def rotate(self, angle, time_step, map_data, sea_level):
        """lorsque le bateau tourne, il conserve sa vitesse
        le bateau tourne moins vite lorsqu'il est à l'arrêt"""

        # bloque la rotation du bateau s'il n'est pas dans l'eau
        height_level = self.get_height_level(map_data)
        if height_level - 1 > sea_level:
            return

        speed_norm = self.dot.speed.get_norm()
        if speed_norm != 0:
            self.orientation += angle * time_step
        else:
            self.orientation += 0.4 * angle * time_step
        self.dot.speed.x = math.cos(self.orientation) * speed_norm * (1 - self.coeff_swivel * abs(angle))
        self.dot.speed.y = math.sin(self.orientation) * speed_norm * (1 - self.coeff_swivel * abs(angle))

    def set_engine_power(self, power):
        """régulateur sur la puissance afin de ne pas dépasser le max"""
        if power <= -self.max_power:
            self.engine_power = -self.max_power
        elif power <= self.max_power:
            self.engine_power = power
        else:
            self.engine_power = self.max_power

    def run(self, time_step, map_data, sea_level):
        """calcul des forces en présence et application de la seconde loi de Newton"""

        sand_friction_force = Force(0, 0)
        water_friction_force = Force(0, 0)

        speed_norm = self.dot.speed.get_norm()
        height_level = self.get_height_level(map_data)

        # forces dépendantes de la vitesse, ainsi, pas de calcul si la vitesse est nulle donc l'orientation none
        temp_orientation = self.dot.speed.get_orientation()
        if temp_orientation is not None:
            if temp_orientation % math.pi != self.orientation % math.pi:
                if speed_norm > 1:
                    self.orientation = temp_orientation
            # freinage du bateau en raison des frottements de l'eau
            water_friction_force = -self.coeff_water_friction * speed_norm * Force(math.cos(temp_orientation),
                                                                                   math.sin(temp_orientation))

            # si le bateau est trop proche du sable, il s'enlisse
            coeff_resistance_sand = (height_level - sea_level) * self.coeff_sand_friction
            if coeff_resistance_sand > 0:
                sand_friction_force = -coeff_resistance_sand * Force(math.cos(temp_orientation),
                                                                     math.sin(temp_orientation))

        # force motrice
        engine_force = self.engine_power * Force(math.cos(self.orientation),
                                                 math.sin(self.orientation))

        resultant = engine_force + water_friction_force + sand_friction_force

        self.dot.run(resultant, time_step)
        if speed_norm < 5 and self.engine_power < 0:
            self.dot.speed = Speed(0, 0)
        self.rect = self.image.get_rect()
        self.rect.center = (self.dot.pos.x, self.dot.pos.y)

    def fire(self, direction_left: bool):
        pass

    def get_damage(self, damage_points):
        self.health -= damage_points

    def get_height_level(self, map_data):
        return map_data.heightMap[int(self.dot.pos.x)][int(self.dot.pos.y)]

    def display_boat(self, screen: pygame.Surface):
        self.image = pygame.transform.rotate(self.base_image, -self.orientation * 180 / math.pi)
        screen.blit(self.image, self.rect)

    def display_health(self, screen: pygame.Surface):
        black = (0, 0, 0)
        green = (65, 225, 77)

        back_rect = pygame.rect.Rect(0, 0, 34, 10)
        back_rect.center = (self.dot.pos.x, self.dot.pos.y - self.rect.height / 2 - 8)
        pygame.draw.rect(screen, black, back_rect)

        front_rect = pygame.rect.Rect(back_rect.x + 1, back_rect.y + 1, 32 * self.health / self.max_health, 8)
        pygame.draw.rect(screen, green, front_rect)

