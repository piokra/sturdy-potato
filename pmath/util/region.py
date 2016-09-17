from ..rndgen.pygen import StdRealUniformGenerator


class Region:
    """ This class describes a region in an abstract space """

    default_generators = [StdRealUniformGenerator()]

    def __init__(self):
        raise NotImplementedError('This is an abstract base class')

    def can_convert_to_hcube(self):
        """
        Returns whether region can be converted to a hcube (by changing the coordinate system)
        :return: True or False
        """
        return NotImplementedError('This is an abstract method')

    def convert_to_hcube(self):
        """
        Converts this region to a hcube (in a different coordinate system)
        :return: ExtendedHCubeRegion or None if impossible
        """
        return NotImplementedError('This is an abstract method')

    def is_inside(self, point):
        """
        Checkss whether point is inside region
        :param point: point in cartesian coordinate system
        :return: True or False
        """

        return NotImplementedError('This is an abstract method')

    def is_inside_native(self, point):
        """
        Checks whether point is inside region
        :param point: point in native coordinate system
        :return: True or False
        """
        return NotImplementedError('This is an abstract method')

    def dimensions(self):
        """ Returns dim of the space in case of G**N sets"""
        return NotImplementedError('This is an abstract method')

    def bounding_hcube(self):
        """
        Returns a hypercube that bounds this region
        :return: HCubeRegion
        """
        return NotImplementedError('This is an abstract method')

    def penetration(self, point):
        """
        Returns a measure of how much the point penetrates the region
        (intuitively how far from the boundary the point is)
        This one is unbound (not normalized)
        :param point penetrating point
        :return: float [0, infty) 0 is no penetration
        """
        return NotImplementedError('This is an abstract method')

    def penetration_normalized(self, point):
        """
        Returns a measure of how much the point penetrates the region
        (intuitively how far from the boundary the point is)
        This one is normalized (eg. penetration/max_penetration)
        :param point penetrating point
        :return: float [0, 1] 0 is no penetration 1 is max penetration
        """
        return NotImplementedError('This is an abstract method')

    def get_random_point(self):
        """
        Returns a random point from the region. Points are generated uniformly.
        :return: Tuple[float]
        """

        rect = self.bounding_hcube()  # type: HCubeRect
        point = rect.get_random_point()
        while not self.is_inside(point):
            point = rect.get_random_point()
        return point
