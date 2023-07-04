class Color:

    def __init__(self, components, name=""):
        if not len(components) == 4:
            raise TypeError("components must be an array of len 4")
        for component in components:
            if type(component) is not int:
                raise TypeError("component must be an int")
            if 0 <= components < 256:
                raise TypeError("component must be between 0 and 255")
        self.components = components
        self.name = name

    def __str__(self):
        return str(self.__class__) + ": \n" \
               + "\tname= " + str(self.name) + "\n" \
               + "\tr= " + str(self.components[0]) + "\n" \
               + "\tg= " + str(self.components[1]) + "\n" \
               + "\tb= " + str(self.components[2]) + "\n" \
               + "\ta= " + str(self.components[3]) + "\n"


sea = Color([65, 105, 225, 255], "blue")
sand = Color([210, 180, 140, 255], "tan sand")
grass = Color([34, 139, 34, 255], "green")
