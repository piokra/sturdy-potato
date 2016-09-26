from optimization.optimization_method import OptimizationMethod, NormalizedFitnessHandler
from optimization.walk import RandomWalk, LevyFlight
from pmath.rndgen.pygen import StdRealUniformGenerator
from pmath.rndgen.util import WeightedSelector
from pmath.util.vector_util import *


class GeneticAlgorithm(OptimizationMethod):
    def __init__(self, p_cross1=0.6, p_cross2=0.3, p_mutation=0.02, elitism=0.1, mu=20, lambdaf=40, region=None):
        super().__init__(region)

        self.p_cross1 = p_cross1
        self.p_cross2 = p_cross2
        self.p_mutation = p_mutation
        self.elitism = elitism
        self.handler = NormalizedFitnessHandler()
        self.epsilon = 10e-12
        self.smallwalk = RandomWalk(scale=0.1)
        self.bigwalk = LevyFlight()
        # self.population_size = mu
        # self.init_population(gen_count=population_size)

        self.mutation_generator = StdRealUniformGenerator()
        self.selector = WeightedSelector()
        self.mutators = dict()
        self.mutator = RandomWalk(walk_generator=NormalDistribution01())

        self.parents = self.unique_parents
        self.candidates = self.mu_and_lambda
        self.mu = mu
        self.lambdaf = lambdaf

    def unique_parents(self):
        return self.selector.population(self.agents, 2, lambda x: 1.1 - self.handler.get_fitness(x))

    def nonunique_parents(self):
        return [self.selector.choose(self.agents, lambda x: 1.1 - self.handler.get_fitness(x)) for i in range(2)]

    def mu_plus_lambda(self, new_pop):
        return self.agents.copy() + new_pop

    def mu_and_lambda(self, new_pop):
        return new_pop

    def set_fitness_function(self, fitness_function):
        super().set_fitness_function(fitness_function)
        self.init_population(gen_count=self.mu)

    def cross1(self, agent1, agent2):
        fit1 = self.handler.get_fitness(agent1)
        fit2 = self.handler.get_fitness(agent2)
        c1 = fit1 / (fit1 + fit2 + self.epsilon)
        agent_temp1 = scl_mul(1 - c1, agent1)
        agent_temp2 = scl_mul(c1, agent2)
        agent = vec_add(agent_temp1, agent_temp2)
        self.mutators[id(agent)] = (1 - c1) * self.mutators[id(agent1)] + c1 * self.mutators[id(agent2)]
        return agent

    def cross2(self, agent1, agent2):
        # agent1 = agent1.copy()
        # agent2 = agent2.copy()

        self.smallwalk.method(agent1, 0)
        self.smallwalk.method(agent2, 0)
        return self.cross1(agent1, agent2)

    def default_mutation(self, agent):
        self.mutator.scale = self.mutators[id(agent)]

    def clean_up_mutators(self):
        new_dict = dict()
        old_dict = self.mutators
        if self.agents is not None:
            for agent in self.agents:
                scale = 0.0
                try:
                    scale = self.mutators[id(agent)]
                except KeyError:
                    scale = self.mutator.walk_generator.get()
                new_dict[id(agent)] = scale
            del old_dict
        self.mutators = new_dict

    def mutation(self, agent1):
        # agent1 = agent1.copy()
        self.bigwalk.method(agent1, 0)
        # return agent1

    def call_methods(self):
        self.clean_up_mutators()
        for agent in self.agents:
            if self.mutation_generator.get() < self.p_mutation:
                self.mutation(agent)
            else:
                self.default_mutation(agent)

        l = self.p_cross1 + self.p_cross2
        p = self.p_cross1 / l

        new_population = []
        for i in range(self.lambdaf):
            parents = self.parents()

            x = self.mutation_generator.get()
            if x < p:
                new_population.append(self.cross1(parents[0], parents[1]))
            else:
                new_population.append(self.cross2(parents[0], parents[1]))

        self.handler.set_population(new_population)
        new_population = self.candidates(new_population)
        new_population = self.selector.population(new_population,
                                                  self.mu - int(len(self.agents) * self.elitism),
                                                  lambda xx: 1.1 - self.handler.get_fitness(xx))
        self.agents.sort(key=self.fitness_function)
        for i in range(int(len(self.agents) * self.elitism)):
            new_population.append(self.agents[i])
        self.agents = new_population
        self.handler.set_population(new_population)

        #        self.handler.refresh()

    def method(self, agent, i):
        pass


class ESMuPlusLambda(GeneticAlgorithm):
    def __init__(self, p_cross1=0.6, p_cross2=0.3, p_mutation=0.02, elitism=0.1, mu=20, lambdaf=40, region=None):
        super().__init__(p_cross1=p_cross1, p_mutation=p_mutation, elitism=elitism, mu=mu, lambdaf=lambdaf,
                         region=region)
        self.parents = self.nonunique_parents
        self.candidates = self.mu_plus_lambda
