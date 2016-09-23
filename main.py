# ga.sex System EXpercki (do Optymalizacji) 

#self.set_function_and_region(parabolaxy, parabolaxy_region)
from gui.test import test
from optimization.genetic import GeneticAlgorithm
from pmath.functions.test_functions import parabolaxy_region, parabolaxy
from pmath.rndgen.util import WeightedSelector

test()
exit()
sel = WeightedSelector()
l = [[1,2],[3,4]]
print(sel.population(l, 1, lambda x: x[0]+x[1]))
r = sel.choose(l, lambda x: 1)
print(r in l)

ga = GeneticAlgorithm(region=parabolaxy_region)
ga.set_fitness_function(parabolaxy)
ga.set_time_limit(3)

agents = ga.start(save=10)

#self.add_result("GA", agents)
