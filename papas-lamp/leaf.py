

import copy
from typing import Union

import build123d
from build123d import *
from build123d.topology import tuplify
from ocp_vscode import *

set_port(3939)

print(build123d.__version__)

class leaf(BasePartObject):
    def __init__(
        self,
        height: float,
        rotation: RotationLike = (0, 0, 0),
        align: Union[Align, tuple[Align, Align, Align]] = (
            Align.CENTER,
            Align.CENTER,
            Align.CENTER,
        ),
        mode: Mode = Mode.ADD,
    ):

        with BuildPart() as liefdoen:
            with BuildSketch() as pedal:
                with BuildLine():
                    b0 = Bezier((0, 200), (80, 197), (75, 80),
                                (100, 80), (180, -72),
                                (190, -210), (0, -180))
                    mirror(about=Plane.YZ)
                make_face()
                scale(by=height / pedal.sketch.bounding_box().size.Y)

            extrude(amount=height/25)

        solid = liefdoen.part.solid()

        super().__init__(
            part=solid, rotation=rotation, align=tuplify(align, 3), mode=mode
        )

    #making a slider


#for visualistation purpose
with BuildPart() as lieafsut:
    leaf(height=30)

show_all(reset_camera=Camera.KEEP)
