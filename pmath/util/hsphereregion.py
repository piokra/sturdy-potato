from pmath.rndgen.advanced import NormalDistribution01
from pmath.util.hcuberegion import HCubeRegion
from pmath.util.region import Region
from pmath.util.vector_util import *


class HSphereRegion(Region):
    def __init__(self, point: List, radius: float):
        self.point = point.copy()
        self.radius = radius
        self.is_zero = True
        low_bound = vec_sub(point, [radius] * len(self.point))
        high_bound = vec_add(point, [radius] * len(self.point))
        self._bounding_hcube = HCubeRegion(low_bound, high_bound)
        for x in point:
            if x != 0:
                self.is_zero = False

        while len(self.point) > len(Region.normal_generators):
            Region.normal_generators.append(NormalDistribution01())

    def is_inside_native(self, point):
        return False

    def dimensions(self):
        return len(self.point)

    def can_convert_to_hcube(self):
        return False

    def is_inside(self, point):
        return dist(point, self.point) <= self.radius

    def penetration(self, point):
        return self.radius - dist(point, self.point)

    def bounding_hcube(self):
        return self._bounding_hcube

    def penetration_normalized(self, point):
        return self.penetration(point) / self.radius
