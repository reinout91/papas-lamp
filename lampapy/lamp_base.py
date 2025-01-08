"""Dit is een script om een lamp te maken voor papa.

Hij wil:
- allemaal bloemetjes boven de eettafel,
- die ook functioneren als een soort spot,
- die open en dicht kunnen,
- in vrolijke kleuren.
"""

from build123d import (
    Align,
    BasePartObject,
    Box,
    BuildLine,
    BuildPart,
    BuildSketch,
    Circle,
    Cylinder,
    Helix,
    Location,
    Locations,
    Mode,
    Plane,
    PolarLocations,
    RegularPolygon,
    RigidJoint,
    Rot,
    RotationLike,
    Sphere,
    export_step,
    sweep,
)
from build123d import (
    __version__ as vs,
)
from build123d.topology import tuplify
from ocp_vscode import Camera, set_port, show_all

set_port(3939)

print(vs)


class HelixShape(BasePartObject):
    def __init__(
        self,
        height: float,
        radius: float,
        pitch: float,
        threadradius: float,
        rotation: RotationLike = (0, 0, 0),
        align: Align | tuple[Align, Align, Align] = (
            Align.CENTER,
            Align.CENTER,
            Align.CENTER,
        ),
        mode: Mode = Mode.ADD,
    ) -> None:
        with BuildPart() as p:
            with BuildLine():
                l1 = Helix(pitch=pitch, height=height, radius=radius)
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


with BuildPart(Plane.XY) as regular_polygon_platform:
    """De bovenkant van de lamp is in vorm van een polygon.
    Later is dit uitgebreid met scharnieren en een hulst om de
    binnenste koker in te draaien"""
    g = 18
    n_sides = 7

    with Locations((0, 0, 0)):
        with PolarLocations(
            radius=g, count=n_sides, start_angle=360 / (2 * n_sides)
        ) as dl:
            Box(11, 6, 6.6, align=(Align.MAX, Align.CENTER, Align.MIN))
            Box(
                11,
                3,
                6.6,
                align=(Align.MAX, Align.CENTER, Align.MIN),
                mode=Mode.SUBTRACT,
            )
            with Locations((-3.5, 0, 3.5)) as pl:
                Cylinder(
                    2,
                    6,
                    360,
                    (90, 0, 0),
                    (Align.CENTER, Align.CENTER, Align.CENTER),
                    Mode.SUBTRACT,
                )

                [
                    RigidJoint(
                        label=f"revojoint_{i}",
                        joint_location=Location(loc.position, loc.orientation)
                        * Rot(90, 0, 0),
                    )
                    for i, loc in enumerate(pl.locations)
                ]
        Cylinder(8.3, 6.6, align=(Align.CENTER, Align.CENTER, Align.MIN))
        Cylinder(
            6, 6.6, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT
        )
        with BuildLine():
            l1 = Helix(
                pitch=(6.6 * 7) / 3,
                height=6.6,
                radius=7,
            )
        with BuildSketch(Location((0, 0, 0), (0, 0, 0))):
            myface = RegularPolygon(7, 7)
        sweep(
            [myface],
            l1,
            multisection=True,
            is_frenet=True,
            binormal=False,
            mode=Mode.SUBTRACT,
        )

""" visualisatie"""
# Delete the original parts, only the copied instances remain,.


show_all(reset_camera=Camera.KEEP)

export_step(regular_polygon_platform.part, "regular_polygon_platform.step")
