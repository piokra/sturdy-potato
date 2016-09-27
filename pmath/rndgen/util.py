from typing import List

from pmath.functions.base_function import MathFunction, MathException
from pmath.functions.elementary_functions import Polynomial
from pmath.util.integrator import CallableIntegrator
from pmath.util.mcintegrator import DivideAndConquerMC
from pmath.util.roots import NewtonMethod, RootFinder
from .generator import Generator
from .pygen import StdRealUniformGenerator


class NDimGenerator(Generator):
    def __init__(self, generators: List):
        self.generators = generators.copy()

    def get(self):
        return list(generator.get() for generator in self.generators)


class WeightedSelector:
    """ Utillity class for weighted selected random element from a list and random weighted population"""

    def __init__(self, uniform_generator=StdRealUniformGenerator()):
        self.generator = uniform_generator

    def choose(self, l: List, key=None):
        """
        Selects random weighted element
        :param l: List with elements
        :param key: This is a function that returns the weight of element. If key is none element is assesed as weight
        :return: Random weighted element from list
        """
        weighted = []
        sum = 0
        for el in l:
            weight = el
            if key is not None:
                weight = key(el)
            if weight < 0:
                raise ValueError('Negative weight. Aborting')
            sum += weight
            weighted.append((sum, el))

        rand = self.generator.get() * sum
        # print("rand:", rand)
        # print("sum:", sum)
        for el in weighted:
            #print(el[0])
            if el[0] >= rand:
                return el[1]


    def population(self, l: List, k: int, key=None):
        ret = []
        l = l.copy()
        for i in range(k):
            obj = self.choose(l, key)
            l.remove(obj)
            ret.append(obj)
        return ret


class InverseCDFGenerator(Generator):
    def __init__(self, func: MathFunction, solver: RootFinder = None, generator: Generator = None, low: List = None):
        self.func = func

        self.generator = generator
        if generator is None:
            gens = []
            for i in range(self.func.input_dim()):
                gens.append(StdRealUniformGenerator())
            self.generator = NDimGenerator(gens)

        if low is None:
            low = (-999,) * self.func.input_dim()

        self.solver = solver
        if solver is None:
            self.solver = NewtonMethod(10e-3)
        try:
            self.integral = self.func.integral()
        except MathException:
            self.integral = CallableIntegrator(low, DivideAndConquerMC(4, 4, 0.01),
                                               self.func)


    def get(self):
        return self.solver.solve(self.integral - Polynomial(self.generator.get()))
