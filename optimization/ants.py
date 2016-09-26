import random
from typing import Tuple

from optimization.optimization_method import OptimizationMethod
from pmath.graphs.graphs import Graph
from pmath.graphs.graphs import Node
from pmath.rndgen.util import WeightedSelector


class ArtificalAnts_TS(OptimizationMethod):
    def __init__(self,
                 graph: Graph,
                 p=1.0,  # pheromone multiplier
                 d=1.5,  # distance multiplier
                 pheromone=0.04,  # pheromone added per walk
                 # distance=1, # this can either be a float or F(value, iter, time)
                 evaporation: float = 0.96,  # this can either be a float or F(value, iter, time)
                 normalized_time: bool = False,  # whether time and iter should be normalized to max
                 dist_name: str = "dist",
                 pheromone_name: str = "pheromone",
                 ):
        super().__init__()
        self.p = p
        self.d = d
        self.graph = graph
        graph["line"] = self.pheromone_name
        self.dist_name = dist_name
        self.pheromone_name = pheromone_name
        self.evaporation = evaporation
        self.normalized_time = normalized_time
        # self.visited_cities = [] # Cities visited by each ant
        self.ants = []
        self.init_population()
        self.selector = WeightedSelector()
        self.pheromone = pheromone

    def value_iter_time(self, value):
        iter = self.iteration
        if self.iteration_limit > 0:
            iter /= self.iteration_limit
        time = self.runtime
        if self.time_limit < float('inf'):
            time /= self.time_limit
        return value, iter, time

    def update_graph(self):
        for node in self.graph.nodes:
            for edge in node.edges:
                edge[self.pheromone_name] *= self.evaporation

    def init_population(self, agents=None, gen_count=30):
        if agents is None:
            self.ants = [[random.choice(self.graph.nodes), set()] for i in range(gen_count)]
        else:
            self.ants = agents

    def edge_weight(self, agent, edge):
        if edge.second in agent[1]:
            return 0

        return (edge[self.pheromone_name]) * self.p + (1 - edge[self.dist_name]) * self.d

    def call_methods(self):

        for i, ant in enumerate(self.ants):
            ant = ant  # type: Tuple[Node, set]
            ant[1].add(ant[0])
            edge = self.selector.choose(ant[0].edges, key=self.edge_weight)
            next_city = edge.second
            new_set = ant[1]
            edge[self.pheromone_name] = min(1, edge[self.pheromone_name] + self.pheromone)

            if len(ant[1]) == len(self.graph.nodes):
                new_set = set()

            new_ant = (next_city, new_set)
            self.ants[i] = new_ant
        self.update_graph()
