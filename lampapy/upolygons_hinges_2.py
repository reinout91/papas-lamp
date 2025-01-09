"""Miriam is trying build123. Miriam wants to make a lamp for papa.

26--05-2024
"""

from build123d import (
    Align,
    BasePartObject,
    BuildLine,
    BuildPart,
    BuildSketch,
    Circle,
    Cylinder,
    Helix,
    Hole,
    Locations,
    Mode,
    Plane,
    RotationLike,
    sweep,
)
from build123d.build_common import validate_inputs
from build123d.topology import tuplify
from ocp_vscode import Camera, set_port, show_all

set_port(3939)


class HelixShape(BasePartObject):
    def __init__(
        self,
        threadradius: float,
        rotation: RotationLike = (0, 0, 0),
        align: Align | tuple[Align, Align, Align] = (
            Align.CENTER,
            Align.CENTER,
            Align.CENTER,
        ),
        mode: Mode = Mode.ADD,
    ) -> None:
        context: BuildPart = BuildPart._get_context(self)
        validate_inputs(context, self)

        with BuildPart() as p:
            with BuildLine():
                l1 = Helix(3, 30, 5.2)
            with BuildSketch(Plane(origin=l1 @ 0, z_dir=l1 % 0)):
                Circle(threadradius)
            sweep()

        solid = p.part.solid()

        super().__init__(
            part=solid, rotation=rotation, align=tuplify(align, 3), mode=mode
        )


with BuildPart() as Outer_Tube:
    with Locations((0, 0, 60 / 2)):
        Cylinder(6, 30)
        Hole(5.1)
        HelixShape(threadradius=0.2, mode=Mode.SUBTRACT)

show_all(reset_camera=Camera.KEEP, render_joints=True, render_mates=True)
