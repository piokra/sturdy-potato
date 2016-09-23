import uuid
from typing import Iterable, Tuple

from pmath.rndgen.generator import Generator
from pmath.rndgen.pygen import StdRealUniformGenerator


class Edge:
    def __init__(self, first: 'Node', second: 'Node', sym: bool = True, **kwargs):
        self.first = first
        self.second = second
        if kwargs is None:
            kwargs = dict()
        self.values = kwargs.copy()


class Node:
    def __init__(self, **kwargs):
        if kwargs is None:
            kwargs = dict()
        self.values = kwargs.copy()
        self.edges = []  # type List[Edge]

    def add_edge(self, second: 'Node', symmetrical: bool = True, **kwargs) -> 'Edge':
        if second is None:
            raise ValueError("The other node must be a valid node")
        new_edge = Edge(self, second, symmetrical, **kwargs)
        self.edges.append(new_edge)
        if symmetrical:
            sym_edge = Edge(second, self, symmetrical)
            sym_edge.values = self.values
            second.edges.append(sym_edge)
        return new_edge

    def drop_edge(self, second: 'Node', symmetrical: bool = True):
        rem = None
        for edge in self.edges:
            if edge.second is second:
                rem = edge
                break
        if rem is not None:
            self.edges.remove(rem)

        if symmetrical:
            rem.second.drop_edge(self, False)

    def delete_value(self, name):
        try:
            del self.values[name]
        except KeyError:
            pass
        for edge in self.edges:
            try:
                del edge.values[name]
            except KeyError:
                pass

    def is_connected(self, second: 'Node'):
        for edge in self.edges:
            if edge.second is second:
                return True
        return False


def _dfs_helper(node: Node, func, visited: str):
    node.values[visited] = True
    if func is not None:
        func(node)
    for edge in node.edges:
        values = edge.second.values  # type: dict
        try:
            values[visited]
        except KeyError:
            _dfs_helper(edge.second, func, visited)


def dfs(graph: 'Graph', node: 'Node' = None, func=None):
    visited = str(uuid.uuid4())
    if node is None:
        node = graph.nodes[0]
    _dfs_helper(node, func, visited)
    graph.delete_value(visited)


class Graph:
    def __init__(self, **kwargs):
        self.nodes = []
        if kwargs is None:
            kwargs = dict()
        self.values = kwargs.copy()

    def delete_value(self, name):
        for node in self.nodes:
            node.delete_value(name)


class RandomGraphGenerator(Generator):
    def __init__(self, node_count: int = 10, edge_chance: float = 0.3,
                 continuous: bool = True, symmetrical: bool = True,
                 node_values: Iterable[Tuple[str, Generator]] = None,
                 edge_values: Iterable[Tuple[str, Generator]] = None):
        self.node_count = node_count
        self.edge_chance = edge_chance
        self.continuous = continuous
        self.symmetrical = symmetrical
        self.node_values = node_values
        self.edge_values = edge_values
        self.default_generator = StdRealUniformGenerator()

    def gen_edge(self, node, other_node):
        edge = node.add_edge(other_node, self.symmetrical)
        if self.edge_values is not None:
            for name, generator in self.edge_values:
                if generator is None:
                    generator = self.default_generator
                edge.values[name] = generator.get()

    def get(self):
        ret = Graph()
        nodes = [Node() for i in range(self.node_count)]
        ret.nodes = nodes
        if self.node_values is not None:
            for name, generator in self.node_values:
                if generator is None:
                    generator = self.default_generator
                for node in nodes:
                    node.values[name] = generator.get()

        for node in nodes:
            for other_node in nodes:
                if not node.is_connected(other_node) and node is not other_node:
                    val = self.default_generator.get()
                    if val <= self.edge_chance:
                        print("Gen edge")
                        self.gen_edge(node, other_node)

        if self.continuous:
            for node in nodes:
                for other_node in nodes:
                    def colour(nnode: Node):
                        nnode.values["colour"] = True

                    dfs(ret, node, colour)
                    try:
                        # node.values["colour"]
                        other_node.values["colour"]
                    except KeyError:
                        self.gen_edge(node, other_node)
                    ret.delete_value("colour")

        return ret
