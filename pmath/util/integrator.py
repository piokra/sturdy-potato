from typing import List

from pmath.util.hcuberegion import HCubeRegion
from .region import Region
from ..functions.base_function import MathFunction


class Integrator:
    def __init__(self):
        raise NotImplementedError("This is an abstract base class")

    def integrate(self, func: MathFunction, bounds: Region) -> float:
        raise NotImplementedError("This is an abstract base class")


class CallableIntegrator(MathFunction):
    """
        This class represent the integral from a to x
        (in more dimensions the integral over the hcube built
        between a and x)

    """

    def __init__(self, low, integrator: Integrator, func: MathFunction):
        self.low = low
        self.integrator = integrator
        self.func = func

    def _derivative(self, variable):
        return self.func

    def input_dim(self) -> int:
        return self.func.input_dim()

    def output_dim(self) -> int:
        return self.func.output_dim()

    def _integral(self, variable):
        return CallableIntegrator(self.low, self.integrator, self)

    def __str__(self):
        return "Integral from: {} to: X of: {}".format(str(self.low), str(self.func))

    def __call__(self, arguments: List[float]) -> float:
        for low, high in zip(self.low, arguments):

            if low > high:
                return 0
        region = HCubeRegion(self.low, arguments)
        return self.integrator.integrate(self.func, region)

    def parameter_count(self):
        return 0
