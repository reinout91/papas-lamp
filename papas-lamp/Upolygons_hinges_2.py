'''
26--05-2024
Miriam is trying build123. Miriam wants to make a lamp for papa.
'''

from ocp_vscode import Camera, set_port, show, show_all

set_port(3939)
from typing import Union

from build123d import *
from build123d.build_common import validate_inputs
from build123d.topology import Solid, tuplify

class HelixShape(BasePartObject):

    def __init__(
        self,
        length: float,
        radius: float,
        threadradius: float,
        rotation: RotationLike = (0, 0, 0),
        align: Union[Align, tuple[Align, Align, Align]] = (
            Align.CENTER,
            Align.CENTER,
            Align.CENTER,
        ),
        mode: Mode = Mode.ADD,
    ):
        context: BuildPart = BuildPart._get_context(self)
        validate_inputs(context, self)

        with BuildPart() as p:
            with BuildLine ():
                l1 = Helix(3,30,5.2)
            with BuildSketch(Plane(origin=l1 @ 0, z_dir=l1 % 0)) as example_7_section:
                Circle(threadradius)
            sweep()

        solid = p.part.solid()

        super().__init__(
            part=solid, rotation=rotation, align=tuplify(align, 3), mode=mode
        )


with BuildPart() as Outer_Tube:
    with Locations((0,0,60/2)):
        Cylinder(6,30)
        Hole(5.1)
        HelixShape(10,10, threadradius = 0.2, mode=Mode.SUBTRACT)

show_all(reset_camera=Camera.KEEP, render_joints = True, render_mates = True)
