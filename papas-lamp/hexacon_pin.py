"""
Dit is de pin
"""

import copy
from typing import Union

import build123d
from build123d import *
from build123d.topology import tuplify
from ocp_vscode import *
from build123d_ease import align


set_port(3939)

print(build123d.__version__)


with BuildPart() as hexacon_pin:
    with BuildLine ():
        l1 = Helix(pitch =(6.6*7)/3, height = 3*6.6, radius = 7-0.2, direction = (0,0,1))
    with BuildSketch(Location((0,0,0),(0,0,0))):
        myface = RegularPolygon(7-0.2,7)
    axle = sweep([myface], l1, multisection=True, is_frenet=True, binormal=False)
    with BuildSketch(hexacon_pin.faces().sort_by(Axis.Z)[0]) as ex24_sk:
        RegularPolygon(7-0.2, 7)
    with BuildSketch(ex24_sk.faces()[0].offset(-(0.5))) as bub:
        Circle(7-0.2)
    loft(ruled = True)
    with Locations(hexacon_pin.faces().sort_by(Axis.Z)[0]) as ref1:
        Cylinder(8.3,4.6, align=align.BOTTOM)
        Cone(7, 5.2,2, align=align.BOTTOM, mode = Mode.SUBTRACT)
        Cylinder(5.2,4.6, align=align.BOTTOM, mode = Mode.SUBTRACT)
        Cone(7-0.2, 5,2, align=align.BOTTOM)
        Cylinder(5,4.6, align=align.BOTTOM)
    with Locations(hexacon_pin.faces().sort_by(Axis.Z)[0]):
        Cylinder(8.3,1, align=align.BOTTOM)
        Cone(5.2, 7,2, align=align.BOTTOM, mode=Mode.SUBTRACT)
        Cone(5, 5.9,1, align=align.BOTTOM)
    with Locations(hexacon_pin.faces().sort_by(Axis.Z)[0]):
        Cylinder(8.3,1, align=align.BOTTOM)
        Cylinder(5.9+0.2,1, align=align.BOTTOM, mode = Mode.SUBTRACT)
        Cylinder(5.9,1, align=align.BOTTOM)
    with Locations(hexacon_pin.faces().sort_by(Axis.Z)[0]):
        with PolarLocations(radius=18, count=7, start_angle=360 / (2 * 7)) as dl:
            Box(11, 6, 6.6, align=(Align.MAX, Align.CENTER, Align.MAX))
            Box(11, 3, 6.6, align=(Align.MAX, Align.CENTER, Align.MAX), mode = Mode.SUBTRACT)
            with Locations((-3.6, 0, -3.2)) as pl:
                Cylinder(
                    2,
                    6,
                    360,
                    (90, 0, 0),
                    align.CENTER,
                    Mode.SUBTRACT,
                )


export_step(hexacon_pin.part, "hexacon_pin.step")
show_all(reset_camera=Camera.KEEP)

