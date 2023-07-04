import random
import noise
import numpy


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


class ColorMap:
    """Transformation de la heightmap en image RGB"""

    sea = [65, 105, 225]
    sand = [210, 180, 140]
    grass = [34, 139, 34]

    def __init__(self, generate_map: GenerateMap):
        self.map = generate_map
        self.colored_map = numpy.zeros((self.map.mapSize[0], self.map.mapSize[1], 3))

    def get_color_map_array(self, sea_level, sand_height):
        """La couleur est définie en fonction de la valeur de la heightmap et du sea level"""
        for i in range(self.map.mapSize[0]):
            for j in range(self.map.mapSize[1]):
                if self.map.heightMap[i][j] < sea_level:
                    self.colored_map[i][j] = ColorMap.sea
                elif self.map.heightMap[i][j] < (sea_level + sand_height):
                    self.colored_map[i][j] = ColorMap.sand
                else:
                    self.colored_map[i][j] = ColorMap.grass
        return self.colored_map
