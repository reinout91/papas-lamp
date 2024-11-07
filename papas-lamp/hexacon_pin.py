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


#Delete the original parts, only the copied instances remain,.


# Inner_Tube.color=Color("red")


with BuildPart(Plane.XY) as hexacon_pin:
    with BuildLine ():
        l1 = Helix(pitch =(6.6*7)/3, height = 3*6.6, radius = 7-0.2, )
    with BuildSketch(Location((0,0,0),(0,0,0))):
        myface = RegularPolygon(7-0.2,7)
    sweep([myface], l1, multisection=True, is_frenet=True, binormal=False)
show_all(reset_camera=Camera.KEEP)

export_step(hexacon_pin.part, "hexacon_pin.step")