from optimization.genetic import GeneticAlgorithm
from optimization.meadneld import MeadNelderMethod
from optimization.optimization_method import OptimizationMethod
from pmath.functions.base_function import MathFunction, Variables
from pmath.functions.elementary_functions import Polynomial
from pmath.rndgen.util import WeightedSelector
from pmath.util.region import Region


class PerAgentMixer(OptimizationMethod):
    """
    This class provides utility for mixing methods. Every iteration instead of doing one selected method it
    chooses a random method from method pool (Selection is weighted). This process is done for every agent.
    """

    def __init__(self, normalized=True, region: Region = None):
        super().__init__(region=region)
        self.methods = []  # type: List[Tuple[Any, OptimizationMethod]]
        self.normalized = normalized
        self.selector = WeightedSelector()

    def add_method(self, weight, method):
        """
        Add an optimization method to the method pool
        :param weight: This can be either a float or MathFunction(iter, time)
        :param method: Optimization Method
        :return:
        """
        if type(weight) is MathFunction:
            if weight.input_dim() != 2:
                raise ValueError("You must supply a constant weight or F: R^2 -> R")

        self.methods.append((weight, method))

    def get_weight(self, method_tup):
        weight = method_tup[0]
        if issubclass(type(weight), MathFunction):
            iteration = self.iteration
            if self.iteration_limit > 0 and self.normalized:
                iteration /= self.iteration_limit

            time = self.runtime
            if self.time_limit < float('inf'):
                time /= self.time_limit

            weight = weight((iter, time))
        return max(0, weight)

    def method(self, agent, i):
        weight, selection = self.selector.choose(self.methods, self.get_weight)
        selection.set_fitness_function(self.fitness_function)
        selection.agents = self.agents
        selection.region = self.region
        selection.handler.set_population(self.agents)
        selection.method(agent, i)
        self.agents = selection.agents


class PerIterationMixer(PerAgentMixer):
    """
    This class provides utility for mixing methods. Every iteration instead of doing one selected method it
    chooses a random method from method pool (Selection is weighted). This process is once per iteration for all agents.
    """

    def __init__(self, normalized=True, region: Region = None):
        super().__init__(normalized=normalized, region=region)

    def call_methods(self):
        weight, selection = self.selector.choose(self.methods, self.get_weight)
        selection.set_fitness_function(self.fitness_function)
        selection.agents = self.agents
        selection.handler.set_population(self.agents)
        selection.call_methods()
        self.agents = selection.agents


class DownhillGenetic(PerIterationMixer):
    def __init__(self, region: Region = None):
        super().__init__(region=region)
        variables = Variables()
        iter, time = variables.get(2, ["i", "t"])
        gen_schedule = (1.1 @ time) - (Polynomial.X @ time)
        self.add_method(gen_schedule, GeneticAlgorithm())
        self.add_method(0.2, MeadNelderMethod())
