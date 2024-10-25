import copy
from typing import Union

import build123d
from build123d import *
from build123d.topology import tuplify
from ocp_vscode import *


set_port(3939)

print(build123d.__version__)

# specify parameters on base of the hinges
W1 = 6 * MM
H = 6 * MM
H2 = 3.9 * MM
H3 = 4 * MM

with BuildPart() as first:
    with Locations((-10, 0, 0)):
        bla = Box(6, 50, H, align=(Align.MAX, Align.CENTER, Align.CENTER))
        Box(14, 6.1, H2, align=(Align.MIN, Align.CENTER, Align.CENTER))
    with Locations(bla.faces().filter_by(Axis.Y)[-1].center_location):
        bla = Box(H2, 6, 10, align=(Align.CENTER, Align.CENTER, Align.MIN))
    with Locations(
        bla.faces().filter_by(Axis.Y)[-1].center_location.position + (0, -1, 0)
    ):
        Cylinder(2.5, H, align=(Align.CENTER, Align.MAX, Align.CENTER))

    Cylinder(2, 999, mode=Mode.SUBTRACT)
    max_fillet = first.part.max_fillet(
        first.edges().filter_by(Axis.Z), tolerance=0.2, max_iterations=20
    )
    fillet(objects=first.edges().filter_by(Axis.Z), radius=max_fillet)

with BuildPart() as second:
    with Locations((-2, 0, 0)):
        bla = Box(10, W1, H, align=(Align.MIN, Align.CENTER, Align.CENTER))
    with Locations(bla.faces().filter_by(Axis.X)[-1].center_location.position):
        bla = Box(10, W1, H, align=(Align.MIN, Align.CENTER, Align.CENTER))
        Box(
            80,
            30,
            H3,
            align=(Align.MAX, Align.CENTER, Align.CENTER),
            mode=Mode.SUBTRACT,
        )
    cyl = Cylinder(1.9, H, align=(Align.MIN, Align.CENTER, Align.CENTER))
    with Locations(bla.faces().filter_by(Axis.X)[-1].center_location.position):
        bla = Box(7, W1, H2, align=(Align.MIN, Align.CENTER, Align.CENTER))
    with Locations(
        bla.faces().filter_by(Axis.X)[-1].center_location.position + (-1, 0, 0)
    ):
        Cylinder(2, H, align=(Align.MAX, Align.CENTER, Align.CENTER))
    max_fillet = second.part.max_fillet(
        second.edges().filter_by(Axis.Z), tolerance=2, max_iterations=20
    )
    fillet(objects=second.edges().filter_by(Axis.Z), radius=max_fillet)

j1 = RevoluteJoint(label="first_hole", to_part=first.part)
j2 = RigidJoint(
    label="second_pin", to_part=second.part, joint_location=Location(cyl.center())
)
j2.connect_to(j1, angle=20)

del bla
del cyl
del j1
del j2
second.part.color = "red"


show_all(reset_camera=Camera.KEEP)

comp_hinge_arms = Compound((first.part, second.part))
export_step(comp_hinge_arms, "hinge_lever.step")
