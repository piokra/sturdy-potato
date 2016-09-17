from operator import add, sub, mul, truediv, pow
from typing import List

import pmath.functions.ho_function


# Variable = None


class MathException(ValueError):
    def __init__(self, str="MO module: MathException"):
        super().__init__(str)


class MathFunction:
    """ Class outlining expected math function interface """

    def __init__(self):
        self.derivative_cache = [None] * self.input_dim()
        self.integral_cache = [None] * self.input_dim()

    def input_dim(self) -> int:
        """ Outputs number of input dimensions """
        raise NotImplementedError("This method must be overridden")

    def output_dim(self) -> int:
        """ Outputs number of output dimensions """
        raise NotImplementedError("This method must be overridden")

    def parameter_count(self) -> int:
        """ Outputs number of parameters """
        raise NotImplementedError("This method must be overridden")

    def __call__(self, arguments: List[float]) -> float:
        """
            Calls the object
            Please notice that the parameters are defaulted to 0
            if none are provided.
            :returns float
        """
        raise NotImplementedError("This method must be overridden")

    def derivative(self, variable=None):
        if variable is None:
            variable = Variable(0, 1)
        if self.derivative_cache[variable.num % self.input_dim()] is None:
            self.derivative_cache[variable.num % self.input_dim()] = self._derivative(variable)
        return self.derivative_cache[variable.num % self.input_dim()]

    def integral(self, variable=None):
        if variable is None:
            variable = Variable(0, 1)
        if self.integral_cache[variable.num % self.input_dim()] is None:
            self.integral_cache[variable.num % self.input_dim()] = self._integral(variable)
        return self.integral_cache[variable.num % self.input_dim()]

    def _derivative(self, variable):
        """
            This procedure returns derivative of this instance of MathFunction
            :param variable:
            :raises MathException if no known derivative
            :returns MathFunction
        """
        raise NotImplementedError("This method must be overridden")

    def _integral(self, variable):
        """
            This procedure returns integral of this instance of MathFunction
            :param variable:
            :raises MathException if no known integral
            :returns MathFunction
        """
        raise NotImplementedError("This method must be overridden")

    def is_constant(self, variable):
        return False

    def is_zero(self):
        return False

    def is_variable(self, variable):
        return False

    def __str__(self):
        raise NotImplementedError("This method must be overridden")

    def __add__(self, other):
        return pmath.functions.base_function.FunctionSum(self, other)

    def __sub__(self, other):
        return pmath.functions.base_function.FunctionSubtraction(self, other)

    def __mul__(self, other):
        return pmath.functions.base_function.FunctionMultiplication(self, other)

    def __pow__(self, power, modulo=None):
        return pmath.functions.base_function.FunctionPower(self, power)

    def __matmul__(self, other):
        return pmath.functions.base_function.FunctionComposiiton(self, other)

    def __truediv__(self, other):
        return pmath.functions.base_function.FunctionDivision(self, other)


class HOBinaryFunction(MathFunction):
    """ (f op g)(...) """

    def __init__(self, f: MathFunction, g: MathFunction, operation):
        self.f = f  # type: MathFunction
        self.g = g  # type: MathFunction
        super().__init__()
        self.op = operation

        if (f.input_dim() != g.input_dim()):
            raise ValueError('Mismatched function inputs')

        if (f.output_dim() != g.output_dim()):
            raise ValueError('Mismatched function outputs')

    def output_dim(self) -> int:
        return self.f.output_dim()

    def input_dim(self) -> int:
        return self.f.input_dim()

    def __call__(self, arguments: List[float]) -> float:
        return self.op(self.f(arguments),
                       self.g(arguments))


class FunctionSum(HOBinaryFunction):
    """ (f + g) """

    def __init__(self, f: MathFunction, g: MathFunction):
        super().__init__(f, g, add)

    def _derivative(self, variable):
        return self.f._derivative(variable) + self.g._derivative(variable)

    def _integral(self, variable):
        return self.f._integral(variable) + self.g._integral(variable)

    def __str__(self):
        return "(" + str(self.f) + ") + (" + str(self.g) + ")"


class FunctionSubtraction(HOBinaryFunction):
    """ (f + g) """

    def __init__(self, f: MathFunction, g: MathFunction):
        super().__init__(f, g, sub)

    def _derivative(self, variable):
        return self.f._derivative(variable) - self.g._derivative(variable)

    def _integral(self, variable):
        return self.f._integral(variable) - self.g._integral(variable)

    def __str__(self):
        return "(" + str(self.f) + ") - (" + str(self.g) + ")"


class FunctionMultiplication(HOBinaryFunction):
    """ (f * g) """

    def __init__(self, f: MathFunction, g: MathFunction):
        super().__init__(f, g, mul)

    def _derivative(self, variable):
        return self.f._derivative(variable) * self.g + self.g._derivative(variable) * self.f

    def _integral(self, variable):
        raise MathException("No generic analytic integration method known :(")

    def __str__(self):
        return "(" + str(self.f) + ") * (" + str(self.g) + ")"


class FunctionDivision(HOBinaryFunction):
    """ (f / g) """

    def __init__(self, f: MathFunction, g: MathFunction):
        super().__init__(f, g, truediv)

    def _integral(self, variable):
        raise MathException("No generic analytic integration method known :(")

    def _derivative(self, variable):
        return (self.f._derivative(variable) * self.g - self.g._derivative(variable) * self.f) / (self.g * self.g)

    def __str__(self):
        return "(" + str(self.f) + ") / (" + str(self.g) + ")"


class FunctionPower(HOBinaryFunction):
    """ (f ** g) """

    def __init__(self, f: MathFunction, g: MathFunction):
        super().__init__(f, g, pow)

    def _integral(self, variable):
        raise MathException("No generic analytic integration method known :(")

    def _derivative(self, variable):
        g = self.g
        f = self.f
        from pmath.functions.elementary_functions import Polynomial
        one = Polynomial([1])
        from pmath.functions.elementary_functions import Log
        return g * (f ** (g - one)) * f._derivative(variable) + \
               (f ** g) * ((Log()) @ f) * g._derivative(variable)

    def __str__(self):
        return "(" + str(self.f) + ") ** (" + str(self.g) + ")"


class FunctionComposiiton(MathFunction):
    """ (f o g) """

    def __init__(self, f: MathFunction, g: MathFunction):
        self.f = f
        self.g = g
        super().__init__()
        if (f.input_dim() != g.output_dim()):
            raise ValueError('For function composition f: X->Y, g: Z->W Z must be Y')

    def __call__(self, arguments: List[float]) -> float:
        return self.f(
            [self.g(arguments)])

    def __str__(self):
        return "(" + str(self.f) + ") o (" + str(self.g) + ")"

    def _derivative(self, variable):
        """ (f o g)' = g' * (f' o g)
        :param variable:
        """
        return self.g._derivative(variable) * FunctionComposiiton(self.f._derivative(variable), self.g)

    def _integral(self, variable):
        if self.g.is_constant(variable):
            return variable * self

        if self.g.is_variable(variable):
            return self.f.integral(variable) @ variable

        raise MathException("No generic analytic integration method known :(")

    def input_dim(self) -> int:
        return self.g.input_dim()

    def output_dim(self) -> int:
        return self.f.output_dim()



class Variable(MathFunction):
    def __init__(self, num: int, max: int, letter=None):
        self.num = num
        self.max = max
        if letter is None:
            letter = "[{}]".format(self.num)
        self.letter = letter

    def is_variable(self, variable):
        return self.num == variable.num

    def is_constant(self, variable):
        return self.num != variable.num

    def __call__(self, arguments: List[float]) -> float:
        return arguments[self.num]

    def _derivative(self, variable=None):
        return pmath.functions.elementary_functions.Polynomial.XX @ self

    def __str__(self):
        return self.letter

    def input_dim(self) -> int:
        return self.max

    def output_dim(self) -> int:
        return 1


class Variables:
    def __init__(self):
        self.first = True

    def get(self, max, letters: List[str] = None):
        if not self.first:
            raise ValueError('This object can only generate one tuple variables')
        self.first = False
        if letters is None:
            return tuple(Variable(i, max) for i in range(max))
        if len(letters) != max:
            raise ValueError('Length of letters is not the same as max argument')
        return tuple(Variable(i, max, letters[i]) for i in range(max))
