"""

    F(x) = 0 solving module

"""
from pmath.functions.base_function import MathFunction
from pmath.util.hcuberegion import HCubeRegion
from pmath.util.region import Region


class RootFinder:
    def __init__(self):
        raise NotImplementedError("This is an abstract base method")

    def solve(self, func: MathFunction, region: Region, start):
        raise NotImplementedError("This is an abstract base method")


class NewtonMethod(RootFinder):
    def __init__(self, precision: float = 0.01, fail_step=100):
        """
        Init newton method
        :param precision:  This is the requested precision described as abs(f(x)) < precision
        :param fail_step: How many steps to stop
        """
        self.precision = precision
        self.fail_step = fail_step

    def solve(self, func: MathFunction, region: Region = None, start=None):
        if region is None:
            region = HCubeRegion((0,)*func.input_dim(), (1,)*func.input_dim())

        start = region.get_random_point()
        derivative = func.derivative()
        value = func(start)
        print(derivative)
        print(func)
        dvalue = derivative(start)

        step = 0
        while abs(value) > self.precision or self.fail_step == step:
            print(value)
            # todo: replace array/tuple with vector class
            for i in range(func.input_dim()):
                # todo: this only works in r^1. Fix with partial deriviation
                try:
                    start[i] = start[i] - value / dvalue
                except (ZeroDivisionError, OverflowError):
                    start = region.get_random_point()
            value = func(start)
            dvalue = derivative(start)
            #print(value, dvalue)
            step += 1
        return start
