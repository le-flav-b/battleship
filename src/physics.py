class Force:
    """Classe Force (exprimée en Newton)"""

    def __init__(self, x_force, y_force):
        self.x = x_force
        self.y = y_force

    def __add__(self, other):
        """somme de deux forces, si type différents: erreur"""
        if type(other) is Force:
            res = Force(self.x + other.x,
                        self.y + other.y)
            return res
        else:
            raise TypeError("unsupported operand type(s) for +: " + str(type(self)) + " and " + str(type(other)))

    def __mul__(self, other):
        """multiplication d'une force par un scalaire"""
        if (type(other) is int) or (type(other) is float):
            res = Force(self.x * other,
                        self.y * other)
            return res
        else:
            raise TypeError("unsupported operand type(s) for +: " + str(type(self)) + " and " + str(type(other)))

    def __rmul__(self, other):
        return self * other

    def __str__(self):
        return str(self.__class__) + ": \n"\
               + "\tx= " + str(self.x) + "\n"\
               + "\ty= " + str(self.y)


class Acceleration:

    def __init__(self, x_acc, y_acc):
        self.x = x_acc
        self.y = y_acc

    def __str__(self):
        return str(self.__class__) + ": \n"\
               + "\tx= " + str(self.x) + "\n"\
               + "\ty= " + str(self.y)


class Speed:

    def __init__(self, x_speed, y_speed):
        self.x = x_speed
        self.y = y_speed

    def __str__(self):
        return str(self.__class__) + ": \n" \
               + "\tx= " + str(self.x) + "\n" \
               + "\ty= " + str(self.y)


class Pos:

    def __init__(self, x_pos, y_pos):
        self.x = x_pos
        self.y = y_pos

    def __str__(self):
        return str(self.__class__) + ": \n"\
               + "\tx= " + str(self.x) + "\n"\
               + "\ty= " + str(self.y)


class Dot:
    """Point mobile en mécanique classique"""

    def __init__(self, pos: Pos, speed: Speed, mass):
        self.pos = pos
        self.speed = speed
        self.mass = mass

    def move(self, acceleration: Acceleration, time_step):
        """ne pas appeler cette fonction, passer par un Bilan Des Forces et utiliser la méthode run()"""
        self.pos.x += 0.5 * acceleration.x * time_step ** 2 + self.speed.x * time_step
        self.pos.y += 0.5 * acceleration.y * time_step ** 2 + self.speed.y * time_step

        self.speed.x += acceleration.x * time_step
        self.speed.y += acceleration.y * time_step

    def run(self, resultant: Force, time_step):
        """calcule le déplacement du point mobile"""
        acceleration = Acceleration(resultant.x / self.mass,
                                    resultant.y / self.mass)
        self.move(acceleration, time_step)

    def __str__(self):
        return str(self.__class__) + ": \n"\
               + "\tpos.x= " + str(self.pos.x) + "\n"\
               + "\tpos.y= " + str(self.pos.y) + "\n" \
               + "\tspeed.y= " + str(self.speed.y) + "\n" \
               + "\tspeed.y= " + str(self.speed.y) + "\n" \
               + "\tmass= " + str(self.mass) + "\n"
