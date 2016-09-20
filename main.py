from time import perf_counter

from optimization.optimization_method import SimulatedAnnealing, NormalizedFitnessHandler, DefaultFitnessHandler, \
    PenalizedRegionOperator, TabooRegionOperator
from pmath.functions.base_function import Variables
from pmath.functions.elementary_functions import Polynomial, Exp, Sin, Cos
from pmath.rndgen.util import InverseCDFGenerator
from pmath.util.hcuberegion import HCubeRegion
from pmath.util.integrator import CallableIntegrator
from pmath.util.mcintegrator import DivideAndConquerMC
from gui.test import test

if __name__ == "__main__":
    test()
    # var = Variables()
    # x, y = var.get(2,["x", "y"])
    # fsin = Sin()
    # fpol = Polynomial([1,2,1])
    # print(fsin+fpol)
    # f = (Sin() @ x) * (Cos() @ y)
    # print(f([2,3]))



def swag():
    pass

'''
if __name__ == "__main__":
    fh = NormalizedFitnessHandler()
    fh.set_fitness_function(Polynomial([0, 1]))
    x, y, z = [0], [1], [2]
    fh.penalize(x, 7)
    fh.set_population([x, y, z])
    fh.sort()
    for agent in fh.top_k_agents(3):
        print(fh.get_fintess(agent))

if __name__ == "__main__":
    forbidden_region = HCubeRegion([-0.9]*2, [0]*2)
    fro = TabooRegionOperator()
    fro.add_region(forbidden_region)

    sa = SimulatedAnnealing(schedule=Polynomial([1]) / Polynomial([1, 0.01]) + Polynomial([0.0000001]))
    #sa.pre_iteration_operators.append(fro)
    sa.set_time_limit(5)
    fro.parent = sa
    # .set_fitness_function(p)
    vars = Variables()
    t = vars.get(1)[0]
    print((Exp() @ t).integral())
    a = [0] * 7
    print(a)
    p = Polynomial([0.1]) * Exp()  # type MathFunction

    p.integral_cache[0] = p
    print(p.derivative())
    print(p([1]))
    ci = CallableIntegrator([-1], DivideAndConquerMC(4, 4, 0.01), p)
    print(ci([-10]))
    print(p)
    gen = InverseCDFGenerator(p, low=(0,))
    now = perf_counter()
    vars = Variables()
    x, y = vars.get(2, ["x", "y"])
    optimize = Polynomial([1, 2, 1])
    optimize = (optimize @ x) + (optimize @ y)
    sa.set_fitness_handler(DefaultFitnessHandler())
    sa.set_fitness_function(optimize)
    print(sa.start())
    # for i in gen.range(10):
    #    print(i)
    # later = perf_counter()

    # print(later - now)
'''