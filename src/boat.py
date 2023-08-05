import math
import pygame
from src.bullet import Bullet
from src.physics import Dot, Pos, Speed, Force


class Boat(pygame.sprite.Sprite):
    boat_bot_image = pygame.image.load("assets/images/boat_bot.png")

    def __init__(self, screen: pygame.Surface, pos: Pos, speed: Speed, mass, max_power=1000, boat_image=boat_bot_image,
                 *groups):
        """création du bateau, orientation en radians"""

        super().__init__(*groups)

        # boat's mechanics constants
        self.max_power = max_power
        self.coeff_water_friction = 5
        self.coeff_sand_friction = 3000
        self.coeff_swivel = 1e-3

        # boat's mechanics related
        self.engine_power = 0
        self.dot = Dot(pos, speed, mass)
        self.orientation = self.dot.speed.get_orientation()
        if self.orientation is None:
            self.orientation = 0

        # pygame's related
        self.screen = screen
        self.size_image = (48, 16)
        self.base_image = pygame.transform.scale(boat_image, self.size_image)
        self.image = self.base_image
        self.rect = self.image.get_rect()
        self.rect.center = (self.dot.pos.x, self.dot.pos.y)

        # game's mechanics related
        self.max_health = 100
        self.health = self.max_health
        self.bullets_damage = 5
        self.bullet_speed_norm = 300

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

    def run(self, time_step, map_data, sea_level, sand_level):
        """opérations à effectuer à chaque tick"""
        # calcul des forces en présence et application de la seconde loi de Newton
        speed_norm = self.dot.speed.get_norm()
        resultant = self.calcul_resultante(map_data, sea_level, sand_level)
        self.dot.run(resultant, time_step)

        # arrêt du bateau s'il freine et que sa vitesse est faible
        if speed_norm < 5 and self.engine_power < 0:
            self.dot.speed = Speed(0, 0)

        self.rest_in_screen()
        self.image = pygame.transform.rotate(self.base_image, -self.orientation * 180 / math.pi)
        self.rect = self.image.get_rect()
        self.rect.center = (self.dot.pos.x, self.dot.pos.y)
        self.screen.blit(self.image, self.rect)

    def calcul_resultante(self, map_data, sea_level, sand_level):
        """calcul des forces à appliquer au bateau"""
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

        return engine_force + water_friction_force + sand_friction_force

    def rest_in_screen(self):
        """appelée à chaque tick, empeche le bateau de sortir de l'écran"""
        self.dot.pos.x = max(0, min(self.dot.pos.x, self.screen.get_width() - 1))
        self.dot.pos.y = max(0, min(self.dot.pos.y, self.screen.get_height() - 1))

    def fire(self, direction_left: bool) -> Bullet:
        """création d'un boulet de canon, celui-ci est renvoyé afin de constituer une liste de tous les boulets"""
        if direction_left:
            bullet_speed = self.bullet_speed_norm * Speed(math.cos(self.orientation - math.pi / 2),
                                                          math.sin(self.orientation - math.pi / 2))
        else:
            bullet_speed = self.bullet_speed_norm * Speed(math.cos(self.orientation + math.pi / 2),
                                                          math.sin(self.orientation + math.pi / 2))
        bullet = Bullet(self.screen, self, Pos(self.dot.pos.x, self.dot.pos.y), bullet_speed)
        return bullet

    def take_damage(self, damage_points):
        self.health -= damage_points
        if not self.is_still_alive():
            self.kill()

    def is_still_alive(self) -> bool:
        if self.health <= 0:
            return False
        return True

    def get_height_level(self, map_data):
        """renvoie la hauteur du terrain sous le bateau"""
        return map_data.heightMap[int(self.dot.pos.x)][int(self.dot.pos.y)]

    def display_health(self):
        """affiche la barre de vie juste au dessus du bateau"""
        if self.alive():
            black = (0, 0, 0)
            green = (65, 225, 77)

            back_rect = pygame.rect.Rect(0, 0, 40, 10)
            back_rect.center = (self.dot.pos.x, self.dot.pos.y - self.rect.height / 2 - 8)
            pygame.draw.rect(self.screen, black, back_rect)

            front_rect = pygame.rect.Rect(back_rect.x + 1, back_rect.y + 1, 38 * self.health / self.max_health, 8)
            pygame.draw.rect(self.screen, green, front_rect)
