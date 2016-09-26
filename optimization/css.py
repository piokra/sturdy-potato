from optimization.optimization_method import OptimizationMethod, NormalizedFitnessHandler
from pmath.rndgen.pygen import StdRealUniformGenerator
from pmath.util.vector_util import *


class ChargedSystemSearch(OptimizationMethod):
    def normalized_time(self):
        if self.iteration_limit > 0:
            return self.iteration / self.iteration_limit
        if self.time_limit < float('inf'):
            return self.runtime / self.time_limit
        return 0

    def method(self, agent, i):
        while i >= len(self.velocities):
            self.velocities.append([0] * self.fitness_function.input_dim())

        epsilon = 10e-6
        best_agent, = self.handler.top_k_agents(1)
        a = [0] * self.fitness_function.input_dim()
        for j, other_agent in enumerate(self.agents):
            if j != i:
                center = vec_add(agent, other_agent)
                rij = dist(agent, other_agent) / (dist(center, best_agent) + epsilon)
                pij = 0
                # extended probability
                if self.handler.get_fitness(agent) > self.handler.get_fitness(other_agent) or \
                                        (self.handler.get_fitness(other_agent) - self.handler.get_fitness(best_agent)) / \
                                        (self.handler.get_fitness(other_agent) - self.handler.get_fitness(agent)) < \
                                self.generator.get():

                #simple probability
                #if self.handler.get_fitness(agent) > self.handler.get_fitness(other_agent):
                    pij = 1
                if rij < self.a:
                    c = pij * self.handler.get_fitness(other_agent) * rij / (self.a ** 3)
                else:
                    c = pij * self.handler.get_fitness(other_agent) / (rij ** 2)
                diff = vec_sub(other_agent, agent)
                diff = scl_mul(c, diff)
                inp_vec_add(a, diff)
        kv = 0.5 * (1 - self.normalized_time())
        ka = 0.5 * (1 + self.normalized_time())
        randj1 = self.generator.get()
        randj2 = self.generator.get()
        c1 = randj1*ka*(self.dt**2)
        c2 = randj2*kv*self.dt
        a1 = scl_mul(c1, a)
        a2 = scl_mul(c2, self.velocities[i])
        agent_new = vec_add(agent, a1, a2)
        dx = vec_sub(agent_new, agent)
        self.velocities[i] = scl_mul(1/self.dt, dx)

        replace(agent, agent_new)


    def __init__(self, a=1.0, dt=1.0, region=None):
        super().__init__(region=region)
        self.velocities = []
        self.a = a
        self.dt = dt
        self.handler = NormalizedFitnessHandler()
        self.generator = StdRealUniformGenerator()
