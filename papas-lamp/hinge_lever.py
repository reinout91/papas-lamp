import copy
from typing import Union

import build123d
from build123d import *
from build123d.topology import tuplify
from ocp_vscode import *


set_port(3939)

print(build123d.__version__)

# specify parameters on base of the hinges
ideal_layer_height = 0.2 * MM
ideal_vert_gap = 2 * ideal_layer_height

W1 = 6 * MM
H = 6 * MM
H3 = 3 * MM
H2 = H3 - ideal_vert_gap
pin_radius = 1.8 * MM
hole_radius = 2 * MM

macc = (Align.MAX, Align.CENTER, Align.CENTER)
micc = (Align.MIN, Align.CENTER, Align.CENTER)

with BuildPart() as t_hinge:
    with Locations((-10, 0, 0)):
        bla = Box(6, 50, H, align = macc)
        Box(14, 6, H2, align = micc)
    with Locations(bla.faces().filter_by(Axis.Y)[-1].center_location):
        bla = Box(H2, 6, 8, align=(Align.CENTER, Align.CENTER, Align.MIN))
    with Locations(
        bla.faces().filter_by(Axis.Y)[-1].center_location.position + (0, -1, 0)
    ):
        Cylinder(pin_radius, H, align=(Align.CENTER, Align.MAX, Align.CENTER))

    Hole(hole_radius)
    max_fillet = t_hinge.part.max_fillet(
        t_hinge.edges().filter_by(Axis.Z), tolerance=0.2, max_iterations=20
    )
    fillet(objects=t_hinge.edges().filter_by(Axis.Z), radius=max_fillet)

with BuildPart() as shackle:
    with Locations((-2, 0, 0)):
        bla = Box(10, W1, H, align = micc)
    with Locations(bla.faces().filter_by(Axis.X)[-1].center_location.position):
        bla = Box(10, W1, H, align = micc)
        Box(
            80,
            30,
            H3,
            align = macc,
            mode = Mode.SUBTRACT,
        )
    cyl = Cylinder(pin_radius, H, align = micc)
    with Locations(bla.faces().filter_by(Axis.X)[-1].center_location.position):
        bla = Box(7, W1, H2, align = micc)
    with Locations(
        bla.faces().filter_by(Axis.X)[-1].center_location.position + (-1, 0, 0)
    ):
        Cylinder(pin_radius, H, align = macc)
    max_fillet = shackle.part.max_fillet(
        shackle.edges().filter_by(Axis.Z), tolerance = 2, max_iterations = 20
    )
    fillet(objects=shackle.edges().filter_by(Axis.Z), radius=max_fillet)

j1 = RevoluteJoint(label="t_hinge_hole", to_part=t_hinge.part)
j2 = RigidJoint(
    label="shackle_pin", to_part=shackle.part, joint_location=Location(cyl.center())
)
j2.connect_to(j1, angle = 0)

del micc, macc, bla, cyl, j1, j2

shackle.part.color = "red"

show_all(reset_camera=Camera.KEEP)

comp_hinge_arms = Compound((t_hinge.part, shackle.part))
export_step(comp_hinge_arms, "hinge_lever.step")
