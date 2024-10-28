"""
Dit is een script om een lamp te maken voor papa.
Hij wil:
- allemaal bloemetjes boven de eettafel,
- die ook functioneren als een soort spot,
- die open en dicht kunnen,
- in vrolijke kleuren.
"""

import copy
from typing import Union

import build123d
from build123d import *
from build123d.topology import tuplify
from ocp_vscode import *

set_port(3939)

print(build123d.__version__)


class HelixShape(BasePartObject):
    def __init__(
        self,
        height: float,
        radius: float,
        pitch: float,
        threadradius: float,
        rotation: RotationLike = (0, 0, 0),
        align: Union[Align, tuple[Align, Align, Align]] = (
            Align.CENTER,
            Align.CENTER,
            Align.CENTER,
        ),
        mode: Mode = Mode.ADD,
    ):

        with BuildPart() as p:
            with BuildLine ():
                l1 = Helix(pitch = pitch, height = height, radius = radius)
            with BuildSketch(Plane(origin=l1 @ 0, z_dir=l1 % 0)):
                Circle(threadradius)
            with Locations(l1 @ 0):
                Sphere(threadradius)
            with Locations(l1 @ 1):
                Sphere(threadradius)
            sweep()

        solid = p.part.solid()

        super().__init__(
            part=solid, rotation=rotation, align=tuplify(align, 3), mode=mode
        )

tt=0.5


with BuildPart(Plane.XY) as regular_polygon_platform:
    '''De bovenkant van de lamp is in vorm van een polygon.
    Later is dit uitgebreid met scharnieren en een hulst om de binnenste koker in te draaien'''
    g = 18
    n_sides = 7

    with Locations((0,0,tt)):
        with PolarLocations(radius=g, count=n_sides, start_angle=360 / (2 * n_sides)) as dl:
            Box(11, 6, 6.5, align=(Align.MAX, Align.CENTER, Align.MIN))
            Box(11, 3, 6.5, align=(Align.MAX, Align.CENTER, Align.MIN), mode = Mode.SUBTRACT)
            with Locations((-3.5, 0, 3.5)) as pl:
                Cylinder(
                    2,
                    6,
                    360,
                    (90, 0, 0),
                    (Align.CENTER, Align.CENTER, Align.CENTER),
                    Mode.SUBTRACT,
                )


                [RigidJoint(label=f"revojoint_{i}", joint_location=Location(loc.position, loc.orientation)*Rot(90,0,0)) for i, loc in enumerate(pl.locations)]
        Cylinder(8.3, 6.5, align=(Align.CENTER, Align.CENTER, Align.MIN))
        Cylinder(7, 6.5, align=(Align.CENTER, Align.CENTER, Align.MIN), mode = Mode.SUBTRACT)


''' visualisatie'''
#Delete the original parts, only the copied instances remain,.


# Inner_Tube.color=Color("red")

show_all(reset_camera=Camera.KEEP)

export_step(regular_polygon_platform.part, "regular_polygon_platform.step")