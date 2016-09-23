from pmath.functions.base_function import *
from pmath.functions.elementary_functions import *
from pmath.util.hcuberegion import HCubeRegion

_vars = Variables()
_x, _y = _vars.get(2, ["x", "y"])

parabolaxy = (Polynomial([1, 2, 1]) @ _x) + (Polynomial([1, 2, 1]) @ _y)
parabolaxy_region = HCubeRegion([-2, -2], [0, 0])

aluffi_pentiny = (Polynomial([0, 0.1, 0.5, 0, 0.25]) @ _x) + (Polynomial([0, 0, 0.5]) @ _y)
aluffi_pentiny_region = HCubeRegion([-10, -10], [10, 10])

bohachevsky1 = (Polynomial([0.7, 0, 1]) @ _x) + (Polynomial([0, 0, 2]) @ _y) + (
    Polynomial([0, -0.3]) @ (Cos() @ (Polynomial([0, 3 * pi]) @ _x))) + (
                   Polynomial([0, -0.4]) @ (Cos() @ (Polynomial([0, 4 * pi]) @ _y)))
bohachevsky1_region = HCubeRegion([-100, -100], [100, 100])

bohachevsky2 = (Polynomial([0.3, 0, 1]) @ _x) + (Polynomial([0, 0, 2]) @ _y) + (
    Polynomial([0, -0.3]) @ (Cos() @ (Polynomial([0, 3 * pi]) @ _x)) * (Cos() @ (Polynomial([0, 4 * pi]) @ _y)))
bohachevsky2_region = HCubeRegion([-50, -50], [50, 50])

becker_lago = (Polynomial.XX @ (Polynomial([-5, 1]) @ (Abs() @ _x))) + (Polynomial.XX @ (Polynomial([-5, 1]) @ (Abs() @ _y)))
becker_lago_region = HCubeRegion([-10, -10], [10, 10])

branin = (Polynomial.XX @ ((Polynomial([0, 5 / pi, -5.1 / (4 * pi ** 2)]) @ _x) + (Polynomial.X @ _y))) + (
Polynomial([10, 10 - 1.25 / pi]) @ (Cos() @ _x))
branin_region = HCubeRegion([-5, 0], [10, 15])

camel = (Polynomial([0, 0, 4, 0, -2.1, 0, 1/3]) @ _x) + (Polynomial([0, 0, -4, 0, 4]) @ _y) + (_x  * _y)
camel_region = HCubeRegion([-5, -5], [5, 5])