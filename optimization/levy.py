from optimization.optimization_method import OptimizationMethod
from pmath.rndgen.advanced import LevyDistribution
from pmath.rndgen.util import NDimGenerator
from pmath.util.vector_util import *


class LevyFlight(OptimizationMethod):
    def __init__(self, mu=0, c=1, mul=1):
        self.generators = []
        self.mu = mu
        self.c = c
        self.mul = mul

    def method(self, agent):
        while len(agent) > len(self.generators):
            self.generators.append(LevyDistribution(mu=self.mu, c=self.c))
            self.generator = NDimGenerator(self.generators)

        change = self.generator.get()
        inp_scl_mul(self.mul, change)
        inp_vec_add(agent, change)
