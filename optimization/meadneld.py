from optimization.optimization_method import OptimizationMethod
from pmath.util.vector_util import *


def unshift_simplex(shifted_simplex, agent):
    center = vec_add(*(vertex for vertex in shifted_simplex))
    center = scl_mul(1 / len(shifted_simplex), center)
    diff = vec_sub(agent, center)
    simplex = [vec_sub(vertex, diff) for vertex in shifted_simplex]

    return simplex


class MeadNelderMethod(OptimizationMethod):
    def __init__(self, size=5, alpha=1.5, gamma=2, rho=0.5, sigma=0.5, region=None):
        super().__init__(region=region)
        self.alpha = alpha
        self.gamma = gamma
        self.rho = rho
        self.sigma = sigma
        self.size = size

        self.simplexes = []  # type: List[List]

    def move_agent(self, shifted_simplex, i):
        center = vec_add(*(vertex for vertex in shifted_simplex))
        center = scl_mul(1 / len(shifted_simplex), center)
        for j, val in enumerate(center):
            self.agents[i][j] = val

    def method(self, agent, i):
        while i >= len(self.simplexes):
            dim = self.fitness_function.input_dim()
            simplex = []
            for j in range(dim):
                vertex = [0]*dim
                vertex[j] = self.size
                simplex.append(vertex)
            simplex.append([0]*dim)
            self.simplexes.append(simplex)

        # print(self.simplexes[i])
        center = vec_add(*(vertex for vertex in self.simplexes[i]))
        center = scl_mul(1 / len(self.simplexes[i]), center)
        # print(center)
        diff = vec_sub(agent, center)
        shifted_simplex = [vec_add(diff, vertex) for vertex in self.simplexes[i]]
        # print(shifted_simplex)
        shifted_simplex.sort(key=self.fitness_function)
        # reflection
        dx = vec_sub(agent, shifted_simplex[-1])
        dx = scl_mul(self.alpha, dx)
        xr_shifted = vec_add(agent, dx)
        if self.fitness_function(shifted_simplex[0]) <= self.fitness_function(xr_shifted) \
                <= self.fitness_function(shifted_simplex[-2]):
            #print("reflecting 1")
            shifted_simplex[-1] = xr_shifted
            self.move_agent(shifted_simplex, i)

            self.simplexes[i] = unshift_simplex(shifted_simplex, self.agents[i])
            return

        # expansion
        if self.fitness_function(xr_shifted) < self.fitness_function(shifted_simplex[0]):
            dx = vec_sub(agent, xr_shifted)
            dx = scl_mul(self.gamma, dx)
            xe_shifted = vec_add(agent, dx)
            if self.fitness_function(xe_shifted) < self.fitness_function(xr_shifted):
                #print("extending")
                shifted_simplex[-1] = xe_shifted
                self.simplexes[i] = unshift_simplex(shifted_simplex, diff)
                return self.move_agent(shifted_simplex, i)
            else:
                #print("reflecting 2")
                shifted_simplex[-1] = xr_shifted
                self.simplexes[i] = unshift_simplex(shifted_simplex, diff)
                return self.move_agent(shifted_simplex, i)
        else:  # contraction
            dx = vec_sub(shifted_simplex[-1], agent)
            dx = scl_mul(self.rho, dx)
            xc_shifted = vec_add(agent, dx)
            if self.fitness_function(xc_shifted) < self.fitness_function(shifted_simplex[-1]):
                #print("contraction")
                shifted_simplex[-1] = xc_shifted
                self.simplexes[i] = unshift_simplex(shifted_simplex, diff)
                return self.move_agent(shifted_simplex, i)
            else:  # shrinking
                #print("shrinking")
                for i in range(len(shifted_simplex) - 1):
                    vertex = shifted_simplex[i + 1]
                    dx = vec_sub(vertex, shifted_simplex[0])
                    dx = scl_mul(self.sigma, dx)
                    new = vec_add(shifted_simplex[0], dx)
                    shifted_simplex[i + 1] = new
                    self.simplexes[i] = unshift_simplex(shifted_simplex, diff)
                    return self.move_agent(shifted_simplex, i)

        raise Exception("This part should not be reached")
