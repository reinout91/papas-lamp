from build123d import (
    MM,
    BasePartObject,
    Bezier,
    BuildLine,
    BuildPart,
    BuildSketch,
    Locations,
    Mode,
    Plane,
    Rectangle,
    RotationLike,
    Triangle,
    extrude,
    make_face,
    mirror,
    scale,
)
from build123d import (
    __version__ as vs,
)
from build123d.topology import tuplify
from build123d_ease import align, top_face_of
from ocp_vscode import set_port

set_port(3939)

print(vs)
length_thinge = 50 * MM
H = 6 * MM
W1 = 6 * MM
H_BLOKJE = W1 / 2


class Leaf(BasePartObject):
    def __init__(
        self,
        height: float,
        rotation: RotationLike = (0, 0, 0),
        mode: Mode = Mode.ADD,
    ) -> None:
        with BuildPart() as liefdoen:
            with BuildSketch() as pedal:
                with BuildLine():
                    Bezier(
                        (0, 200),
                        (80, 197),
                        (75, 80),
                        (100, 80),
                        (180, -72),
                        (190, -210),
                        (0, -180),
                    )
                    mirror(about=Plane.YZ)
                make_face()
                scale(by=height / pedal.sketch.bounding_box().size.Y)

            extrude(amount=height / 25)

            # clips:
            display_face = top_face_of(liefdoen)
            display_workplane = Plane(
                origin=display_face.center(), x_dir=(1, 1, 0), z_dir=(0, -1, 0)
            )
            with BuildSketch(display_workplane):
                with Locations((H / 3 * 2, 0, 0)):
                    Rectangle(
                        width=H_BLOKJE, height=H_BLOKJE, align=align.ANCHOR_FRONT_LEFT
                    )
                    with Locations((0, H_BLOKJE - H / 3, 0)):
                        Triangle(
                            a=H / 3,
                            b=H / 3,
                            C=90,
                            rotation=90,
                            align=align.ANCHOR_FRONT_LEFT,
                        )
                    mirror(about=Plane.YZ, mode=Mode.ADD)
            extrude(amount=3, mode=Mode.ADD, both=True)

        solid = liefdoen.part.solid()

        super().__init__(
            part=solid, rotation=rotation, align=tuplify(align, 3), mode=mode
        )


# visualisation purpose
with BuildPart() as leaf_view:
    leaf(height=30)
show_all(reset_camera=Camera.KEEP)
