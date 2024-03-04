
from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
from build123d import *
set_port(3939)

from itertools import product
import copy

d = 4
n = 6
obj = Sphere(d/2) - Plane.YZ * Cylinder(d/4, 3*d)

s = range(0, n*d, d)
obj = [copy.copy(obj).locate(Pos(l)) for l in product(s, s, s)]

show_object(obj)

