import random

from optimization.optimization_method import OptimizationMethod
from optimization.walk import LevyFlight
from pmath.util.region import Region
from pmath.util.vector_util import replace


class CuckooSearch(OptimizationMethod):
    def __init__(self, population_size=20, pa=0.7, region: Region = None):
        super().__init__(region=region)
        self.handler = None
        self.walker = LevyFlight()
        self.pa = pa
        self.population_size=population_size

    def call_methods(self):
        flights = min(len(self.agents), self.pa*len(self.agents))

        for i in range(int(flights)):
            agent = random.choice(self.agents)
            candidate = agent.copy()

            self.walker.method(candidate,0)
            if self.fitness_function(candidate) < self.fitness_function(agent):
                replace(agent, candidate)

        self.agents.sort(key=self.fitness_function)
        self.agents = self.agents[0:int(len(self.agents)*(1-self.pa))]
        new_agents = [self.region.get_random_point() for i in range(self.population_size-len(self.agents))]
        self.agents += new_agents

