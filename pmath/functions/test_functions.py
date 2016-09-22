from pmath.functions.base_function import *
from pmath.functions.elementary_functions import *
from pmath.util.hcuberegion import HCubeRegion

_vars = Variables()
_x, _y = _vars.get(2, ["x", "y"])

<<<<<<< HEAD
parabolaxy = (Polynomial([1,2,1]) @ _x) + (Polynomial([1,2,1]) @ _y)
=======
parabolaxy = (Polynomial([1, 2, 1]) @ _x) + (Polynomial([1, 2, 1]) @ _y)
>>>>>>> piotr
parabolaxy_region = HCubeRegion([-2, -2], [0, 0])
