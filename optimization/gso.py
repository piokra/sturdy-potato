from optimization.optimization_method import OptimizationMethod, NormalizedFitnessHandler
from optimization.walk import RandomWalk, NormalDistribution01
from pmath.rndgen.util import WeightedSelector
from pmath.util.region import Region
from pmath.util.vector_util import dist, vec_sub, inp_scl_mul, inp_vec_add


class GlowwormSwarmOptimization(OptimizationMethod):
    def __init__(self, stepsize=0.2, r0=1, rho=0.4, gamma=0.6, beta=0.08, nt=5, l0=5, region: Region = None):
        super().__init__(region=region)
        self.handler = NormalizedFitnessHandler()
        self.r0 = r0
        self.rho = rho
        self.gamma = gamma
        self.beta = beta
        self.nt = nt
        self.l0 = l0
        self.luciferin_levels = {}
        self.radii = {}
        self.inited = False
        self.selector = WeightedSelector()
        self.stepsize = stepsize
        self.gauss_walker = RandomWalk(walk_generator=NormalDistribution01())
    def call_methods(self):
        if not self.inited:
            for glowworm in self.agents:
                self.luciferin_levels[id(glowworm)] = self.l0
                self.radii[id(glowworm)] = self.r0
                self.inited = True

        for i, glowworm in enumerate(self.agents):
            self.luciferin_levels[id(glowworm)] *= (1 - self.rho)
            self.luciferin_levels[id(glowworm)] += self.gamma * self.handler.get_fitness(glowworm)

        for i, glowworm in enumerate(self.agents):
            func = lambda x: dist(x, glowworm) <= self.radii[id(glowworm)] and \
                                           self.handler.get_fitness(glowworm) >= self.handler.get_fitness(x)
            neigbrohood = filter(func, self.agents)
            luciferin_sum = sum([self.luciferin_levels[id(worm)] for worm in neigbrohood])
            neigbrohood = [item for item in self.agents if func(item)]
            #print(func(glowworm))
            candidates = []
            for neigbro in neigbrohood:

                pij = max(10e-6, self.luciferin_levels[id(neigbro)]-self.luciferin_levels[id(glowworm)])
                pij /= luciferin_sum - self.luciferin_levels[id(glowworm)] + 10e-6
                candidates.append((pij, neigbro))
            if len(neigbrohood) == 1:
                self.gauss_walker.scale = self.radii[id(glowworm)]*0.04
                self.gauss_walker.method(glowworm, 0)
            chance, punny_worm = self.selector.choose(candidates, key=lambda x: x[0])
            cdx = self.stepsize/(dist(punny_worm, glowworm) + 10e-6)
            dx = vec_sub(punny_worm, glowworm)
            inp_scl_mul(cdx, dx)
            inp_vec_add(glowworm, dx)
            self.radii[id(glowworm)] = min(self.r0, max(0, self.radii[id(glowworm)]+self.beta*(self.nt - len(neigbrohood))))






