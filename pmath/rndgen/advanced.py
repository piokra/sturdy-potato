from math import sin, cos, log, sqrt, pi, tan

from pmath.functions.elementary_functions import Polynomial, Erf
from pmath.rndgen.util import InverseCDFGenerator
from .generator import Generator
from .pygen import StdRealUniformGenerator


class NormalDistribution(InverseCDFGenerator):
    def __init__(self, mean=0, std=1, solver=None, generator=None, low=None):
        self.mean = mean
        self.std = std
        self.cdf = Polynomial([0.5]) + Polynomial([0.5]) * \
                                       (Erf() @ Polynomial([-mean / (std * sqrt(2)), 1 / (std * sqrt(2))]))
        super().__init__(self.cdf, solver, generator, low)


class NormalDistribution01(Generator):
    """
    This is fast.
    An object of this class generates numbers from Normal Distribution.
    The constructor takes any two Uniform [0,1) number generators to accomplish its goal.
    Uses Box-Muller method.
    """

    def __init__(self, u_gen: Generator = None, v_gen: Generator = None):
        self.mean = 0
        self.std = 1

        if u_gen is None:
            u_gen = StdRealUniformGenerator()
        if v_gen is None:
            v_gen = StdRealUniformGenerator()

        self.uGen = u_gen
        self.vGen = v_gen
        self.first = None
        self.second = None

    def get(self):
        if self.first is None:
            v = self.vGen.get()
            u = self.uGen.get()
            self.first = sqrt(-log(u)) * cos(2 * pi * v)
            self.second = sqrt(-log(v)) * sin(2 * pi * u)
        ret = self.first
        self.first = self.second
        self.second = None
        return ret


class CauchyDistribution(Generator):
    def __init__(self, x0: float = 0, gamma: float = 1, u_gen: Generator = None):
        self.x0 = x0
        self.gamma = gamma
        if self.gamma <= 0:
            raise AttributeError('This generator accepts only positive gammas')

        if u_gen is None:
            u_gen = StdRealUniformGenerator()

        self.UGen = u_gen

    def get(self):
        x = self.UGen.get()  # X ~ U(0,1)
        c = tan(pi * (x - 0.5))  # C ~ Cauchy(0,1)
        return self.gamma * c + self.x0  # C * \gamma + x0 ~ Cauchy(0*gamma + x0, 1*|gamma|) ~ Cauchy(x0, |gamma|)


class LevyDistribution(Generator):
    def __init__(self, mu=0, c=1, n_gen=None):
        self.mu = mu
        self.c = c

        if n_gen is None:
            n_gen = NormalDistribution01()

        self.n_gen = n_gen

    def get(self):
        Y = self.n_gen.get()  # Generate a number from Noraml Dist(mu, sigma)
        Y = (Y - self.n_gen.mean) ** -2  # We now have: (X - mu)**-2 ~ Levy(0,sigma**-2)
        k = self.c * (self.n_gen.std ** 2)
        b = self.mu
        return k * Y + b  # We now have kY + b ~ Levy(0*k+b, 1/sigma2*b)
