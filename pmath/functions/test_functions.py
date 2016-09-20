from pmath.functions.base_function import *
from pmath.functions.elementary_functions import *

_vars = Variables()
_x, _y = _vars.get(2, ["x", "y"])

parabolaxy = (Polynomial([1,2,1]) @ _x) + (Polynomial([1,2,1]) @ _y)