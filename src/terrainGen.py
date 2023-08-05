import random
import noise
import numpy
import pygame.sprite

from src.physics import Pos


class GenerateMap:
    """Génération procédurale du terrain """

    def __init__(self, size=(50, 50), scale=500, octaves=4, persistence=0.6, lacunarity=2.0,
                 x_starting_pos=0, y_starting_pos=0, seed=0):
        """scale : niveau de zoom, 100 dézoomé, 500 zoomé
           octave : lissage fin de la carte, 4 très lisse, 10 dentelé
           persistence :
           lacunarity : lissage large de la carte, 1 très lisse, 3 dentellé
        """
        self.scale = scale
        self.octaves = octaves
        self.persistence = persistence
        self.lacunarity = lacunarity

        self.x_starting_pos = x_starting_pos
        self.y_starting_pos = y_starting_pos

        self.mapSize = size  # size in pixels
        self.heightMap = numpy.zeros(self.mapSize)

        if seed == 0:
            self.seed = random.randint(0, self.mapSize[0])
        else:
            self.seed = seed

        self.generate_map()

    def generate_map(self):
        """Génération de la heightmap par bruit de perlin"""
        for i in range(self.mapSize[0]):
            for j in range(self.mapSize[1]):
                new_i = i + self.y_starting_pos
                new_j = j + self.x_starting_pos

                self.heightMap[i][j] = noise.pnoise3(new_i / self.scale, new_j / self.scale, self.seed,
                                                     octaves=self.octaves,
                                                     persistence=self.persistence, lacunarity=self.lacunarity,
                                                     repeatx=10000000, repeaty=10000000, base=0)
                self.heightMap[i][j] = int((self.heightMap[i][j] + 1) * 128)
        return self.heightMap


class ColorMap(pygame.sprite.Sprite):
    """Transformation de la heightmap en image RGB"""

    sea = [65, 105, 225]
    sand = [210, 180, 140]
    grass = [34, 139, 34]

    mask_color_transparent = [0, 0, 255, 0]
    mask_color_opaque = [0, 255, 0, 255]

    def __init__(self, generated_map: GenerateMap, sea_level, sand_height, *groups):
        super().__init__(*groups)
        self.map = generated_map
        self.colored_map = numpy.zeros((self.map.mapSize[0], self.map.mapSize[1], 3), numpy.uint8)
        self.mask_map_nparray = numpy.zeros((self.map.mapSize[0], self.map.mapSize[1], 4), numpy.uint8)

        for i in range(self.map.mapSize[0]):
            for j in range(self.map.mapSize[1]):
                if self.map.heightMap[i][j] < sea_level:
                    self.colored_map[i][j] = ColorMap.sea
                    self.mask_map_nparray[i][j] = ColorMap.mask_color_transparent
                elif self.map.heightMap[i][j] < (sea_level + sand_height):
                    self.colored_map[i][j] = ColorMap.sand
                    self.mask_map_nparray[i][j] = ColorMap.mask_color_transparent
                else:
                    self.colored_map[i][j] = ColorMap.grass
                    self.mask_map_nparray[i][j] = ColorMap.mask_color_opaque

        self.image = pygame.surfarray.make_surface(self.colored_map)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(make_surface_rgba(self.mask_map_nparray))


def make_surface_rgba(array):
    """Returns a surface made from a [w, h, 4] numpy array with per-pixel alpha"""
    shape = array.shape
    if len(shape) != 3 and shape[2] != 4:
        raise ValueError("Array not RGBA")

    # Create a surface the same width and height as array and with per-pixel alpha
    surface = pygame.Surface(shape[0:2], pygame.SRCALPHA, 32)

    # Copy the rgb part of array to the new surface.
    pygame.pixelcopy.array_to_surface(surface, array[:, :, 0:3])

    # Copy the alpha part of array to the surface using a pixels-alpha view of the surface
    surface_alpha = numpy.array(surface.get_view("A"), dtype=numpy.uint8, copy=False)
    surface_alpha[:, :] = array[:, :, 3]

    return surface


class SpawnPoint:

    def __init__(self, generated_map: GenerateMap, sea_level, space_between_spawn_point):
        self.sbsp = space_between_spawn_point
        self.map = generated_map
        self.possible_spawns = numpy.empty((int(self.map.mapSize[0] / self.sbsp), int(self.map.mapSize[1] / self.sbsp), 1),
                                           bool)
        self.nb_spawn_points = 0
        for i in range(len(self.possible_spawns)):
            for j in range(len(self.possible_spawns[0])):
                if self.map.heightMap[i * self.sbsp][j * self.sbsp] < sea_level:
                    self.possible_spawns[i][j] = True
                    self.nb_spawn_points += 1
                else:
                    self.possible_spawns[i][j] = False

    def get_spawn_point(self) -> Pos:
        selected_spawn = random.randint(1, self.nb_spawn_points)
        spawn_points_passed = 0
        for i in range(len(self.possible_spawns)):
            for j in range(len(self.possible_spawns[0])):
                if self.possible_spawns[i][j]:
                    spawn_points_passed += 1
                    if spawn_points_passed == selected_spawn:
                        coordinates = Pos(i * self.sbsp, j * self.sbsp)
                        return coordinates
