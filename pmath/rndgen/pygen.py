from os import urandom
from random import Random

from .generator import Generator


class StdGen(Generator):
    def __init__(self, obj, func, *args):
        """
        Generate values from obj.func()
        :param func: Function to call
        """
        if obj is None:
            raise ValueError('None value passed for obj')
        if func is None:
            raise ValueError('None value passed for func')
        self.obj = obj
        self.func = func
        self.args = args

    def get(self):
        try:
            if self.args is None:
                print(self.obj.random())
                return getattr(self.obj, self.func)()
            else:
                return getattr(self.obj, self.func)(*self.args)
        except ValueError as e:

            return None


class StdRealUniformGenerator(StdGen):
    def __init__(self, seed=None):
        if seed is None:
            seed = int.from_bytes(urandom(8), "little")
        super().__init__(Random(seed), "random")


class StdIntUniformGenerator(StdGen):
    def __init__(self, low, high, seed=None):
        if seed is None:
            seed = int.from_bytes(urandom(8), "little")
        super().__init__(Random(seed), "randint", low, high)


class StdGaussGenerator(StdGen):
    def __init__(self, mean=1, sigma=1, seed=None):
        if seed is None:
            seed = int.from_bytes(urandom(8), "little")
        super().__init__(Random(seed), "gauss", mean, sigma)
        self.mean = mean  # this is only for information
        self.sigma = sigma  # ^ ^ ^
        