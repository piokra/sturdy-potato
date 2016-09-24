from copy import deepcopy
from math import exp, sqrt
from multiprocessing import Pool, cpu_count
from time import perf_counter
from typing import List

from pmath.functions.base_function import MathFunction
from pmath.functions.elementary_functions import Polynomial
from pmath.rndgen.generator import Generator
from pmath.rndgen.pygen import StdRealUniformGenerator
from pmath.rndgen.util import NDimGenerator
from pmath.util.hcuberegion import HCubeRegion
from pmath.util.region import Region


class FitnessHandler:
    def __init__(self):
        self.cache = {}
        self.penalty_cache = {}
        self.iter = 0
        self.population = None  # type: List
        self.fitness_function = None

        self.avg_value = 0.0
        self.best_value = 0.0
        self.highest_change = 0.0
        self.total_change = 0.0
        self.best_agent = None



    def refresh(self):
        self.population.sort(key=self.fitness_function)
        max_change = 0.0
        total_change = 0.0
        avg_fitness = 0.0
        min_fitness = self.fitness_function(self.population[0])

        for agent in self.population:
            fitness = self.fitness_method(agent)
            try:
                prev_fitness = self.cache[id(agent)]
                prev_fitness -= fitness
                if max_change < abs(prev_fitness):
                    max_change = abs(prev_fitness)
                total_change += abs(prev_fitness)
            except KeyError:
                pass
            self.cache[id(agent)] = fitness
            avg_fitness += fitness

        self.avg_value = avg_fitness / len(self.population)
        self.highest_change = max_change
        self.total_change = total_change
        self.iter += 1

    def set_population(self, population):
        """
        Change the population of agents. This also refreshes the fitness value
        :param population:
        :return:
        """
        self.population = population
        self.refresh()

    def sort(self):
        self.population.sort(key=self.get_fitness)

    def get_fitness(self, agent):
        fit = self.cache[id(agent)]
        try:
            pen = self.penalty_cache[id(agent)]
        except KeyError:
            pen = 0.0
        return fit + pen

        raise KeyError("Old value cached. Did you forget to refresh?")

    def set_fitness_function(self, fitness_function):
        self.fitness_function = fitness_function

    def get_average_value(self):
        """
        Returns the average value
        :return:
        """
        return self.avg_value

    def get_best_agent(self):
        return self.population[0]

    def get_best_value(self):
        """
        Returns the best value. (We assume lower is better)
        :return: Best value
        """
        return self.get_fitness(self.get_best_agent())

    def top_k_agents(self, k):
        """
        Returns an iterable of top k agents (top k with lowest fitness function)
        :param k: Number of agents to return
        :return: Iterable of tuples of top k  tuple(agent,value)
        """
        k = min(k, len(self.population))
        return self.population[:k]

    def total_abschange_vw(self):
        """
        Returns sum over abs(fitness_function(agent))
        :return: Total change
        """
        return self.total_change

    def highest_abschange_vw(self):
        """
        Highest change function value wise
        :return:
        """
        return self.highest_change

    def penalize(self, agent, penalty):
        self.penalty_cache[id(agent)] = penalty

    def fitness_method(self, agent):
        raise NotImplementedError('This is an abstract base method')


class DefaultFitnessHandler(FitnessHandler):
    def __init__(self):
        super().__init__()

    def fitness_method(self, agent):
        return self.fitness_function(agent)


class NormalizedFitnessHandler(FitnessHandler):
    epsilon = 10e-6

    def __init__(self):
        super().__init__()

    def fitness_method(self, agent):
        max = self.fitness_function(self.population[-1])
        min = self.fitness_function(self.population[0])
        fit = self.fitness_function(agent)
        return (fit - min) / (max - min + NormalizedFitnessHandler.epsilon)


class OptimizationMethod:
    def __init__(self, region: Region = None, generator: Generator = None):
        self.region = region  # todo generalize this to abstract sets (eg graph sets)
        self.iteration_limit = -1
        self.time_limit = float('+inf')
        self.low_value_limit = float('-inf')
        self.high_value_limit = float('+inf')
        self.limit_set = False
        self.generator = generator
        self.pre_iteration_operators = []
        self.post_iteration_operators = []

        self.fitness_function = None  # type: MathFunction
        self.processing_start = None
        self.agents = None  # type: List

        self.highest_change_limit_vw = float('-inf')
        self.highest_total_change_limit_vw = float('-inf')
        self.consecutive_stagnant_iters_limit_vw = 10e6

        self.started = False
        self.finished = False
        self.allow_async_execution = False  # True
        self.pool = None  # Pool(cpu_count())

        self.iteration = 0
        self.handler = NormalizedFitnessHandler()  # type: FitnessHandler

        self.stagnant_single_turns = 0
        self.stagnant_sum_turns = 0
        self.dead_agents = []
        self.new_agents = []
        self.agents_to_replace = []

        self.runtime = 0.0

    def set_time_limit(self, seconds: float):
        """
        Limit the execution of a method by real world time elapsed
        :param seconds: Seconds to stop after
        :return: self
        """
        self.time_limit = seconds
        self.limit_set = True
        return self

    def set_iteration_limit(self, iterations: int):
        """
        Limits the execution of a method by iteration count
        :param iterations: Number of iterations to stop after
        :return: self
        """
        self.iteration_limit = iterations
        self.limit_set = True
        return self

    def set_value_limit(self, low_limit: float, high_limit: float):
        """
        Limits the execution of a method by the fitness function values
        If the function is below low_limit or above high_limit (we guess it divereged)
        the method stops
        :param low_limit: Low limit
        :param high_limit: High limit
        :return: self
        """
        self.low_value_limit = low_limit
        self.high_value_limit = high_limit
        self.limit_set = True
        return self

    def set_stagnant_limit_vw(self, highest_change: float, highest_total_change: float, stagnant_iterations: int):
        """
        Limits the execution of a method by the change of fitness function value.
        If the absolute change of function fails to go above given limit consecutively for given amount of turns
        the method stops
        :param highest_change: Lowest acceptable fitness function change (For the most changing agent)
        :param highest_total_change: Lowest acceptable total fitness change
        :param stagnant_iterations: Stagnant turns to stop after
        :return: self
        """
        self.highest_change_limit_vw = highest_change
        self.highest_total_change_limit_vw = highest_total_change
        self.consecutive_stagnant_iters_limit_vw = stagnant_iterations
        return self

    def set_fitness_function(self, fitness_function):
        """
        Sets fitness function by calling a
        :param fitness_function:
        :return:
        """
        self.fitness_function = fitness_function
        if self.handler is not None:
            self.handler.set_fitness_function(fitness_function)

    def set_fitness_handler(self, fitness_handler: FitnessHandler):
        """
        Change fitness handler to a given one, also sets fitness function to the one bound to this object
        :param fitness_handler: Fitness handler to set
        :return: self
        """
        self.handler = fitness_handler
        self.handler.set_fitness_function(self.fitness_function)
        return self

    def call_methods(self):
        if self.allow_async_execution:
            for i, agent in enumerate(self.agents):
                if self.allow_async_execution:
                    self.pool.apply(self.method, agent, i)

            self.pool.join()
        else:
            for i, agent in enumerate(self.agents):
                self.method(agent, i)

    def do_iteration(self):
        if not self.started:
            raise RuntimeError("This method must be started with self.start()")

        for operator in self.pre_iteration_operators:
            for agent in self.agents:
                operator(agent)

        self.call_methods()

        for operator in self.post_iteration_operators:
            for agent in self.agents:
                operator(agent)

        if self.handler is not None:
            self.handler.refresh()
        return self.agents

    def init_population(self, agents=None, gen_count=1):
        if agents is not None:
            self.agents = agents
            return

        if self.region is None:
            self.region = HCubeRegion([0] * self.fitness_function.input_dim(), [1] * self.fitness_function.input_dim())

        if self.generator is None:
            generators = list(StdRealUniformGenerator() for i in range(self.fitness_function.input_dim()))
            self.generator = NDimGenerator(generators)

        self.agents = [self.region.get_random_point() for i in range(gen_count)]
        if self.handler is not None:
            self.handler.set_population(self.agents)

    def method(self, agent, i):
        raise NotImplementedError("This has to be overloaded to do method specific operations")

    def start(self, save=None):
        """
        Starts execution of the method
        :param save: save agent state after save iterations:
        :return: List of tuples of saved agents
        """
        saved = []
        start_time = perf_counter()
        self.started = True
        if self.agents is None:
            self.init_population()
        while True:

            agents = self.do_iteration()

            if self.iteration == self.iteration_limit:
                saved.append(agents)
                return saved

            if self.consecutive_stagnant_iters_limit_vw == self.stagnant_single_turns:
                saved.append(agents)
                return saved

            if self.consecutive_stagnant_iters_limit_vw == self.stagnant_sum_turns:
                saved.append(agents)
                return saved

            if self.low_value_limit > self.handler.get_best_value():
                saved.append(agents)
                return saved

            if self.high_value_limit < self.handler.get_best_value():
                saved.append(agents)
                return saved

            if self.handler.highest_abschange_vw() < self.highest_change_limit_vw:
                self.stagnant_single_turns += 1
            else:
                self.stagnant_single_turns = 0

            if self.handler.total_abschange_vw() < self.highest_total_change_limit_vw:
                self.stagnant_sum_turns += 1
            else:
                self.stagnant_sum_turns = 0
            if save is not None:
                if self.iteration % save == 0:
                    saved.append(deepcopy(agents))
                    # return saved

            self.runtime = perf_counter() - start_time
            if self.runtime > self.time_limit:
                saved.append(deepcopy(agents))
                return saved

            self.iteration += 1
            for agent in self.dead_agents:
                if agent in self.agents:
                    self.agents.remove(agent)

            for agent in self.new_agents:
                self.agents.append(agent)

            for old, new in self.agents_to_replace:
                index = self.agents.index(old)
                self.agents[index] = new

            self.agents_to_replace.clear()
            self.dead_agents.clear()
            self.new_agents.clear()

    def set_async(self, allow=True, cpus=cpu_count()):
        """
        Set policy for async self.method call.
        Default its on so you don't have to call it, unless you want to change the number of cpus
        :param allow: True of False
        :param cpu_cnt:
        :return: self
        """
        self.allow_async_execution = allow
        if self.allow_async_execution:
            self.pool = Pool(cpus)
        return self

    def reset(self):
        """
        Resets start and finish variables.
        :return:
        """
        self.started = False
        self.finished = False
        self.iteration = 0
        return self

    def kill_agent(self, agent):
        self.dead_agents.append(agent)

    def add_agent(self, agent=None):
        if agent is None:
            if self.region is None:
                self.region = HCubeRegion([0] * self.fitness_function.input_dim(),
                                          [1] * self.fitness_function.input_dim())
        agent = self.region.get_random_point()

        self.new_agents.append(agent)

    def replace_agent(self, to_replace, new_agent):
        self.agents_to_replace.append((to_replace, new_agent))

class SimulatedAnnealing(OptimizationMethod):
    epsilon = 10e-9

    def __init__(self, k=0.08, T0: float = 100., step: float = 0.1, schedule: MathFunction = None,
                 region: Region = None,
                 generator: Generator = None):
        super().__init__(region=region, generator=generator)
        if schedule is None:
            schedule = Polynomial([1]) / Polynomial([1, 0.005]) + Polynomial([SimulatedAnnealing.epsilon])

        self.schedule = schedule

        # self.region = region

        self.schedule = schedule
        self.k = k
        self.T0 = T0
        self.step = 1
        self.succ = 0.
        self.generator_auto = False
        self.accepter = StdRealUniformGenerator()
        self.prev = float('inf')

    def method(self, agent, i):
        mul = self.schedule([self.succ])
        step = self.step * sqrt(mul)
        temp = self.T0 * mul
        # print(mul, step, temp)
        change = self.generator.get()
        candidate = agent.copy()
        for i in range(len(candidate)):
            # todo replace this in a way to allow non generators (0,1) to work
            candidate[i] += (change[i] - 0.5) * step
        try:
            penalty = self.handler.penalty_cache[id(agent)]
        except KeyError:
            penalty = 0.0

        value = self.fitness_function(candidate)
        if exp((self.prev - value + penalty) / (self.k * temp)) > self.accepter.get():
            self.prev = value
            prev = agent
            for i in range(len(self.agents[0])):
                agent[i] = candidate[i]
                prev = agent
        self.succ += 1

    def set_fitness_function(self, fitness_function):
        super().set_fitness_function(fitness_function)

        if self.generator is None or self.generator_auto:
            self.generator_auto = True
            gens = []
            for i in range(fitness_function.input_dim()):
                gens.append(StdRealUniformGenerator())
            self.generator = NDimGenerator(gens)
        return self


class Operator:
    def __init__(self, parent: OptimizationMethod = None):
        self.parent = parent

    def __call__(self, agent):
        raise NotImplementedError('This is an abstract base method')


class RegionOperator(Operator):
    def __init__(self):
        super().__init__()
        self.regions = []  # type: List[Region]

    def set_regions(self, regions: List[Region]):
        self.regions = regions

    def add_region(self, region: Region):
        self.regions.append(region)


class TabooRegionOperator(RegionOperator):
    def __init__(self):
        super().__init__()

    def __call__(self, agent):
        for region in self.regions:
            if region.is_inside(agent):
                self.parent.kill_agent(agent)
                self.parent.add_agent()


class NormalizedPenalizedRegionOperator(RegionOperator):
    def __init__(self, func):
        super().__init__()
        self.func = func

    def __call__(self, agent):
        if self.parent is None or self.parent.handler is None:
            raise "No parent or no handler"
        for region in self.regions:
            pen = region.penetration_normalized(agent)
            if pen > 0:
                self.parent.handler.penalize(agent, self.func(pen))


class PenalizedRegionOperator(RegionOperator):
    def __init__(self, func):
        super().__init__()
        self.func = func

    def __call__(self, agent):
        if self.parent is None or self.parent.handler is None:
            raise "No parent or no handler"
        for region in self.regions:
            pen = region.penetration(agent)
            if pen > 0:
                self.parent.handler.penalize(agent, self.func(pen))
