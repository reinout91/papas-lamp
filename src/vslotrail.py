from build123d import *
from build123d import tuplify
from ocp_vscode import *
from typing import Union


class VSlotLinearRailProfile(BaseSketchObject):
    """Sketch Object: OpenBuilds V Slot Linear Rail Profile

    Args:
        rotation (float, optional): angles to rotate objects. Defaults to 0.
        align (Union[Align, tuple[Align, Align]], optional): align min, center, or max of object.
            Defaults to (Align.CENTER, Align.CENTER).
        mode (Mode, optional): combination mode. Defaults to Mode.ADD.
    """

    _applies_to = [BuildSketch._tag]

    def __init__(
        self,
        rotation: float = 0,
        align: tuple[Align, Align] = (Align.CENTER, Align.CENTER),
        mode: Mode = Mode.ADD,
    ):
        with BuildSketch() as groove:
            with BuildLine():
                Polyline(
                    (3.69, 0),
                    (3.9, 0.21),
                    (3.9, 2.8393398282202034),
                    (6.560660171779773, 5.5),
                    (8.2, 5.5),
                    (8.2, 3.125),
                    (8.545, 3.125),
                    (10, 4.58),
                    (10, 0),
                )
                mirror(about=Plane.XZ)
            make_face()

        with BuildSketch() as ext20x20:
            RectangleRounded(20, 20, 0.5)
            Circle(2.1, mode=Mode.SUBTRACT)
            with PolarLocations(0, 4):
                add(groove.face(), mode=Mode.SUBTRACT)

        super().__init__(obj=ext20x20.sketch, rotation=rotation, align=align, mode=mode)
class VSlotLinearRail(BasePartObject):
    """Part Object: OpenBuilds V Slot Linear Rail

    Args:
        length (float): box size
        rotation (RotationLike, optional): angles to rotate about axes. Defaults to (0, 0, 0).
        align (Union[Align, tuple[Align, Align, Align]], optional): align min, center,
            or max of object. Defaults to (Align.CENTER, Align.CENTER, Align.MIN).
        mode (Mode, optional): combine mode. Defaults to Mode.ADD.
    """

    _applies_to = [BuildPart._tag]

    def __init__(
        self,
        length: float,
        rotation: RotationLike = (0, 0, 0),
        align: Union[Align, tuple[Align, Align, Align]] = (
            Align.CENTER,
            Align.CENTER,
            Align.MIN,
        ),
        mode: Mode = Mode.ADD,
    ):
        rail = extrude(VSlotLinearRailProfile(), amount=length, dir=(0, 0, 1))
        RigidJoint("test1", rail, Location((10, 0, 0), (0, 90, 0)))
        RigidJoint("test2", rail, Location((0, -10, 50), (90, 0, 0)))
        super().__init__(
            part=rail, rotation=rotation, align=tuplify(align, 3), mode=mode
        )


show(VSlotLinearRailProfile())
show(VSlotLinearRail(100), render_joints=True)