from optimization.optimization_method import OptimizationMethod
from pmath.rndgen.advanced import LevyDistribution
from pmath.rndgen.generator import Generator
from pmath.rndgen.pygen import StdRealUniformGenerator
from pmath.util.vector_util import *


class RandomWalk(OptimizationMethod):
    def __init__(self, scale=1.0, walk_generator:Generator=StdRealUniformGenerator(), region=None):
        super().__init__(region)
        self.walk_generator = walk_generator
        self.scale =scale

    def method(self, agent, i):
        change = random_dir(len(agent))
        inp_scl_mul(self.scale*self.walk_generator.get(), change)
        inp_vec_add(agent, change)

class LevyFlight(RandomWalk):
    def __init__(self, scale=1.0, mu=0, c=1, region=None):
        super().__init__(scale, LevyDistribution(mu,c), region)