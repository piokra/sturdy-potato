# ga.sex System EXpercki (do Optymalizacji) 

#self.set_function_and_region(parabolaxy, parabolaxy_region)
from gui.test import test
from optimization.genetic import GeneticAlgorithm
from pmath.functions.elementary_functions import Polynomial
from pmath.functions.test_functions import parabolaxy_region, parabolaxy, branin_region, branin
from pmath.graphs.graphs import PositionGenerator
from pmath.rndgen.util import WeightedSelector



pg = PositionGenerator(branin_region)
print(pg.points_left())

print(2*Polynomial.XX)
test()
exit()
sel = WeightedSelector()
l = [[1,2],[3,4]]
print(sel.population(l, 1, lambda x: x[0]+x[1]))
r = sel.choose(l, lambda x: 1)
print(r in l)

from optimization.genetic import GeneticAlgorithm
self.set_function_and_region(branin, branin_region, step=0.33)
ga = GeneticAlgorithm(region=branin_region)
ga.set_fitness_function(branin)
ga.set_time_limit(3)

agents = ga.start(save=10)

self.add_result("GA", agents)
