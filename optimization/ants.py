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
                 d=5,  # distance multiplier
                 pheromone=0.4,  # pheromone added per walk for best ant
                 pheromone_min=0.1,  # for worst ant
                 # distance=1, # this can either be a float or F(value, iter, time)
                 evaporation: float = 0.75,  # this can either be a float or F(value, iter, time)
                 normalized_time: bool = False,  # whether time and iter should be normalized to max
                 dist_name: str = "dist",
                 gen_count = 100,
                 pheromone_name: str = "pheromone",
                 ):
        super().__init__(region=None)
        self.p = p
        self.d = d
        self.graph = graph
        self.agents = [graph]
        self.dist_name = dist_name
        self.pheromone_name = pheromone_name
        graph["line"] = self.pheromone_name
        self.evaporation = evaporation
        self.normalized_time = normalized_time
        self.pheromone_min = pheromone_min
        # self.visited_cities = [] # Cities visited by each ant
        self.ants = []
        self.gen_count = gen_count
        self.init_population(gen_count=gen_count)
        self.selector = WeightedSelector()
        self.pheromone = pheromone
        self.handler = None

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
            self.ants = [[random.choice(self.graph.nodes), set(), 0, set()] for i in range(gen_count)]
        else:
            self.ants = agents

    def edge_weight(self, agent, edge):
        if edge.second in agent[1]:
            return 0

        return (edge[self.pheromone_name]) * self.p + (1 - edge[self.dist_name]) * self.d

    def call_methods(self):

        for j in range(len(self.graph.nodes)):
            for i, ant in enumerate(self.ants):
                ant = ant  # type: Tuple[Node, set]

                ant[1].add(ant[0])
                if len(ant[1]) == len(self.graph.nodes):
                    continue
                # print(ant[0])
                # print(ant[0].edges)
                edge = self.selector.choose(ant[0].edges, key=lambda cedge: self.edge_weight(ant, cedge))
                dist = ant[2] + edge[self.dist_name]
                next_city = edge.second
                new_set = ant[1]
                # edge[self.pheromone_name] = min(100, edge[self.pheromone_name] + self.pheromone)
                edge_set = ant[3]
                edge_set.add(edge)
                # if len(ant[1]) == len(self.graph.nodes):
                #    new_set = set()

                new_ant = (next_city, new_set, dist, edge_set)
                self.ants[i] = new_ant

        self.ants.sort(key=lambda x: x[2])

        for i, ant in enumerate(self.ants):
            if i == 0:
                self.graph["best"] = ant[2]
            i = 1 - (i / len(self.ants))
            i *= self.pheromone - self.pheromone_min
            i += self.pheromone_min
            for edge in ant[3]:
                edge[self.pheromone_name] += i
                edge[self.pheromone_name] = min(20, edge[self.pheromone_name])
                # print(edge[self.pheromone_name])
        self.update_graph()
        self.init_population(gen_count=self.gen_count)

