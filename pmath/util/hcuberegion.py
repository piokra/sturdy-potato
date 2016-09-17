from typing import List

from .region import Region
from ..rndgen.pygen import StdRealUniformGenerator


class HCubeRegion(Region):
    def __init__(self, low: List[float], high: List[float]):
        self.ranges = []
        self.dims = min(len(low), len(high))
        for l, h in zip(low, high):
            self.ranges.append((l, h))

        while self.dimensions() > len(Region.default_generators):
            Region.default_generators.append(StdRealUniformGenerator())

    def dimensions(self):
        return self.dims

    def bounding_hcube(self):
        return self

    def is_inside(self, point):
        return super().is_inside(point)

    def penetration(self, point):
        return super().penetration(point)

    def is_inside_native(self, point):
        return self.is_inside(point)

    def can_convert_to_hcube(self):
        return True

    def penetration_normalized(self, point):
        return super().penetration_normalized(point)

    def convert_to_hcube(self):
        return self

    def get_random_point(self):
        point = list(Region.default_generators[i].get() for i in range(self.dims))
        for i, v in enumerate(point):
            point[i] = v * (self.ranges[i][1] - self.ranges[i][0]) + self.ranges[i][0]
        return point

    def random_split(self):
        random_edge = int(Region.default_generators[0].get() * self.dimensions())

        low = [l[0] for l in self.ranges]
        high = [h[1] for h in self.ranges]
        ret = []
        sl, sh = low[random_edge], high[random_edge]
        mid = (sl + sh) / 2
        low[random_edge] = mid
        ret.append(HCubeRegion(low, high))
        low[random_edge] = sl
        high[random_edge] = mid
        ret.append(HCubeRegion(low, high))
        return ret

    def split(self):
        """ This doesnt yet divide into 2^dim hcubes """
        return self.random_split()
