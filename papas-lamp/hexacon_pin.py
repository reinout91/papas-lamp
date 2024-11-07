"""
Dit is de pin
"""

import copy
from typing import Union

import build123d
from build123d import *
from build123d.topology import tuplify
from ocp_vscode import *

set_port(3939)

print(build123d.__version__)


with BuildPart() as ex24:
    with BuildLine ():
        l1 = Helix(pitch =(6.6*7)/3, height = 3*6.6, radius = 7-0.2, direction = (0,0,1))
    with BuildSketch(Location((0,0,0),(0,0,0))):
        myface = RegularPolygon(7-0.2,7)
    axle = sweep([myface], l1, multisection=True, is_frenet=True, binormal=False)
    with BuildSketch(ex24.faces().sort_by(Axis.Z)[0]) as ex24_sk:
        RegularPolygon(7-0.2, 7)
    with BuildSketch(ex24_sk.faces()[0].offset(-(0.5))) as bub:
        Circle(7-0.2)
    loft(ruled = True)
    with Locations(ex24.faces().sort_by(Axis.Z)[0]):
        h = Cone(7-0.2, 5,2, align=(Align.CENTER, Align.CENTER, Align.MIN))
    with Locations(ex24.faces().sort_by(Axis.Z)[0]):
        Cylinder(5,2, align=(Align.CENTER, Align.CENTER, Align.MIN))
    with Locations(ex24.faces().sort_by(Axis.Z)[0]):
        h = Cone(5, 7-0.2,2, align=(Align.CENTER, Align.CENTER, Align.MIN))
    with Locations(ex24.faces().sort_by(Axis.Z)[0]):
        Cylinder(7,1, align=(Align.CENTER, Align.CENTER, Align.MIN))

show_all(reset_camera=Camera.KEEP)