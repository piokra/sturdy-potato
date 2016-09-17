from math import sqrt
from typing import List

from pmath.functions.base_function import MathFunction
from pmath.util.region import Region
from .integrator import Integrator


class BasicMonteCarloIntegrator(Integrator):
    def __init__(self, thousands: int):
        self.thousands = thousands
        self.mean = 0
        self.estim_std = 0
        self.preserve_mean = 0

    def integrate(self, func: MathFunction, bounds: Region) -> float:
        self.estim_std = 0
        if not self.preserve_mean:
            self.mean = 0
            sum = 0
            for i in range(1000):
                sum += func(bounds.get_random_point())
            self.mean = sum / 1000

        for i in range(self.thousands - 1):
            local_std = 0
            local_mean = 0
            for j in range(1000):
                value = func(bounds.get_random_point())
                local_mean += value
                local_std += (self.mean - value) ** 2
            self.mean *= (i + 1) / (i + 2)
            self.mean += local_mean / (1000 * (i + 2))
            self.estim_std += local_std
        self.estim_std = sqrt(self.estim_std / ((self.thousands - 1) * 1000))
        return self.mean


class DivideAndConquerMC(Integrator):
    def __init__(self, thousands: int, max_depth: int, branching_factor: float):
        self.thousands = thousands
        self.max_depth = max_depth
        self.branching_factor = branching_factor
        self.integrator = BasicMonteCarloIntegrator(thousands)

    def integrate_helper(self, func: MathFunction, bounds: List[Region], depth: int):
        # for bound in bounds:
        #    print(bound.ranges)
        # self.integrator.preserve_mean = True
        mean = 0
        for bound in bounds:
            local_mean = self.integrator.integrate(func, bound)
            if self.integrator.estim_std > self.branching_factor and depth != self.max_depth:
                # self.integrator.mean = local_mean
                # local_mean = local_mean * (1 / (len(bounds)+1)) + \
                #             (1 - 1 / (len(bounds)+1)) * self.integrate_helper(func, bound.split(), depth + 1)
                local_mean = self.integrate_helper(func, bound.split(), depth + 1)
            mean += local_mean
        return mean / len(bounds)

    def integrate(self, func: MathFunction, bounds: Region) -> float:
        return self.integrate_helper(func, [bounds], 0)
