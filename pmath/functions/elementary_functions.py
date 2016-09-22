from copy import copy
from math import cos, exp, erf, pi
from math import log
from math import sin
from typing import List

from pmath.functions.base_function import MathFunction


class ElementaryFunction(MathFunction):
    """ This class is a base for all elementary functions"""

    def __init__(self, func):
        super().__init__()
        self.func = func

    def output_dim(self) -> int:
        return 1

    def input_dim(self) -> int:
        return 1

    def __call__(self, arguments: List[float]) -> float:
        return self.func(arguments[0])

    def __str__(self):
        return self.func.__name__


class Polynomial(MathFunction):
    """ This class represents a R->R polynomial of any degree """

    def __init__(self, multipliers: List[float]):
        """

        :param multipliers: the list of multipliers infront of a give x^n where n is index in list eg:
                [0,1,2] === x+2*x**2
        """
        if len(multipliers) == 0:
            multipliers = [0]
        self.multipliers = copy(multipliers)

    def _next_nonzero_mul(self, arr, pos):
        for i in range(len(arr) - pos):
            if arr[i + pos] != 0:
                return arr[i + pos]
        return None

    def __str__(self):
        ret = ""
        for i, mul in enumerate(self.multipliers):
            if mul == 0:
                continue
            ret += str(abs(mul))
            if i != 0:
                ret += "x**" + str(i)
            next_mul = self._next_nonzero_mul(self.multipliers, i + 1)
            if next_mul is not None:
                if (next_mul) > 0:
                    ret += " + "
                else:
                    ret += " - "
        return ret

    def output_dim(self) -> int:
        return 1

    def input_dim(self) -> int:
        return 1

    def _derivative(self, variable):
        new_muls = copy(self.multipliers)
        for i in range(len(new_muls)):
            new_muls[i] *= i
        return Polynomial(new_muls[1:])

    def _integral(self, variable):
        new_muls = [0]
        for i in range(len(self.multipliers)):
            new_muls.append((1 / (1 + i)) * self.multipliers[i])
        return Polynomial(new_muls)

    def __call__(self, arguments: List[float]) -> float:

        ret = 0.
        for i, mul in enumerate(self.multipliers):
            ret += mul * arguments[0] ** i
        return ret


Polynomial.ONE = Polynomial([1])
Polynomial.MINUS_ONE = Polynomial([-1])
Polynomial.X = Polynomial([0, 1])
Polynomial.XX = Polynomial([0, 0, 1])


class Sin(ElementaryFunction):
    def __init__(self):
        super(Sin, self).__init__(sin)

    def _integral(self, variable):
        mo = Polynomial([-1])
        return mo * Cos()

    def _derivative(self, variable):
        return Cos()


class Cos(ElementaryFunction):
    def __init__(self):
        super(Cos, self).__init__(cos)

    def _integral(self, variable):
        return Sin()

    def _derivative(self, variable):
        mo = Polynomial([-1])
        return mo * Sin()


class Log(ElementaryFunction):
    def __init__(self):
        super(Log, self).__init__(log)

    def _integral(self, variable):
        x = Polynomial([0, 1])
        one = Polynomial([1])
        return x * (Log() - one)

    def _derivative(self, variable):
        x = Polynomial([0, 1])
        one = Polynomial([1])
        return one / x


class Exp(ElementaryFunction):
    def __init__(self):
        super().__init__(exp)

    def _integral(self, variable):
        return self

    def _derivative(self, variable):
        return self

class Erf(ElementaryFunction):
    def __init__(self):
        super().__init__(erf)

    def _derivative(self, variable):
        return Polynomial([1/(2*pi)])*(Exp() @ Polynomial([0,0,-0.5]))

class Abs(ElementaryFunction):
    def __init__(self):
        super().__init__(abs)