"""Dit is een script om een lamp te maken voor papa.

Hij wil:
- allemaal bloemetjes boven de eettafel,
- die ook functioneren als een soort spot,
- die open en dicht kunnen,
- in vrolijke kleuren.
"""

import copy

from build123d import (
    Align,
    Axis,
    BasePartObject,
    Box,
    BuildLine,
    BuildPart,
    BuildSketch,
    Circle,
    Color,
    Compound,
    Cylinder,
    Helix,
    Hole,
    Location,
    Locations,
    Mode,
    Plane,
    PolarLocations,
    Polyline,
    RegularPolygon,
    RevoluteJoint,
    RigidJoint,
    Rot,
    RotationLike,
    Sphere,
    extrude,
    make_face,
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


tt = 0.5

with BuildPart(Plane.XY) as regular_polygon_platform:
    """De bovenkant van de lamp is in vorm van een polygon.
    Later is dit uitgebreid met scharnieren en een hulst om de
    binnenste koker in te draaien"""
    g = 10
    n_sides = 7

    with BuildSketch():
        RegularPolygon(radius=g, side_count=n_sides, major_radius=False)
    extrude(amount=tt)

    with Locations((0, 0, tt)):
        with PolarLocations(
            radius=g, count=n_sides, start_angle=360 / (2 * n_sides)
        ) as dl:
            with Locations((0, 1, 0), (0, -1, 0)):
                Box(6, 1, 5, align=(Align.MAX, Align.CENTER, Align.MIN))
            with Locations((-2, 0, 3)) as pl:
                Cylinder(
                    1,
                    3,
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
        Cylinder(4.3, 5, align=(Align.CENTER, Align.CENTER, Align.MIN))
        Cylinder(
            3.8, 5, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT
        )
        HelixShape(
            height=5,
            radius=3.9,
            pitch=2.5,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
            threadradius=0.3,
            mode=Mode.SUBTRACT,
        )

with BuildPart() as pinpart:
    """Dit zijn de armen van de scharnieren"""
    (L, H, B) = (1.5, 10, 1.5)
    pts = [
        (-L, -L),
        (B, -L),
        (B, H),
        (-L, H + L),
    ]

    with BuildSketch(Plane.XY):
        with BuildLine():
            t = Polyline(*pts, close=True)

        make_face()
    extrude(amount=0.4, both=True)
    Cylinder(0.9, 3, 360, (0, 0, 0), Align.CENTER)

    RevoluteJoint(label="j1", axis=Axis.Z)

lever_assembly = Compound(label="lever", children=[pinpart.part])

lever_references = [copy.copy(lever_assembly) for loc in pl.locations]

with BuildPart() as Inner_Tube:
    """ Make an inner tube"""
    with Locations(Location((0, 0, tt), (0, 0, 0))):
        Cylinder(3.6, 10, align=(Align.CENTER, Align.CENTER, Align.MIN))
        Hole(3.2, 30)
        HelixShape(
            height=10,
            radius=3.6,
            pitch=2.5,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
            threadradius=0.3,
            mode=Mode.ADD,
        )


"""Hier wordt de verbindingen gedefineerd"""
for c in range(len(pl.locations)):
    joint_name = f"revojoint_{c}"
    revojoint = regular_polygon_platform.part.joints[joint_name]
    lever_joint = lever_references[c].children[0].joints["j1"]
    revojoint.connect_to(lever_joint, angle=30)


""" visualisatie"""
# Delete the original parts, only the copied instances remain,.
del pinpart
del lever_assembly
lever_references[0].color = Color("red")
lever_references[1].color = Color("blue")
lever_references[2].color = Color("green")

show_all(reset_camera=Camera.KEEP)
