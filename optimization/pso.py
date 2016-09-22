from typing import Tuple

from optimization.optimization_method import OptimizationMethod, DefaultFitnessHandler
from pmath.rndgen.pygen import StdRealUniformGenerator
from pmath.rndgen.util import NDimGenerator
from pmath.util.hcuberegion import HCubeRegion
from pmath.util.vector_util import *


class ParticleSwarmOptimization(OptimizationMethod):
    def __init__(self, region=None, omega=0.3, phil=0.9, phig=0.1):
        super().__init__(region)
        self.omega = 0.3
        self.phil = phil
        self.phig = phig
        self.local_best = []
        self.velocity_region = None  # HCubeRegion
        self.velocities = []
        self.init = False
        self.handler = DefaultFitnessHandler()
        self.generator = None
        self.global_best = None
        self.global_best_value = float('inf')

    def init_method(self):
        self.init = True
        self.handler.set_population(self.agents)
        self.global_best = self.handler.top_k_agents(1)[0]
        generators = [StdRealUniformGenerator() for i in range(self.fitness_function.input_dim())]
        self.generator = NDimGenerator(generators)

    def method(self, agent):
        if not self.init:
            self.init_method()
        global_best = self.handler.top_k_agents(1)[0]
        if self.global_best_value < self.handler.get_best_value():
            global_best = self.global_best
        else:
            self.global_best = global_best
            self.global_best_value = self.handler.get_best_value()

        # print(global_best)
        for i, agent in enumerate(self.agents):
            l_best = self.get_local_best((self.handler.get_fintess(agent), agent), i)
            if not i:
                print(l_best)

            vel = self.velocity(i)
            inp_scl_mul(self.omega, vel)
            gdiff = vec_sub(global_best, agent)
            ldiff = vec_sub(l_best, agent)
            inp_scl_mul(self.phig, gdiff)
            inp_scl_mul(self.phil, ldiff)
            inp_el_wise_mul(gdiff, self.generator.get())
            inp_el_wise_mul(ldiff, self.generator.get())
            inp_vec_add(vel, ldiff)
            inp_vec_add(vel, gdiff)
            self.velocities[i] = vel
            inp_vec_add(agent, vel)

        self.handler.refresh()

    def get_local_best(self, candiate: Tuple[float, List], n: int):
        while n >= len(self.local_best):
            self.local_best.append((float('inf'), None))
        if candiate[0] < self.local_best[n][0]:
            self.local_best[n] = (candiate[0], candiate[1].copy())
            return candiate[1]
        else:
            return self.local_best[n][1]

    def velocity(self, n: int):
        if self.velocity_region is None:
            print("[INFO] PSO: Setting default velocity region.")
            self.velocity_region = HCubeRegion([-1] * self.fitness_function.input_dim(),
                                               [1] * self.fitness_function.input_dim())
        while n >= len(self.velocities):
            self.velocities.append(self.velocity_region.get_random_point())
        return self.velocities[n]
