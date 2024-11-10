import copy
from typing import Union

import build123d
from build123d import *
from build123d.topology import tuplify
from ocp_vscode import *
from build123d_ease import align, back_face_of

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


with BuildPart() as t_hinge:
    with Locations((-W1, -5, 0)):
        bla = Box(W1, 50, H, align = align.RIGHT)
    with Locations((-W1, 0, 0)):
        Box(10, W1, H2, align = align.LEFT)
    with Locations(back_face_of(bla).center_location):
        bla = Box(H2, W1, 8, align=align.BOTTOM)
    with Locations(
       back_face_of(bla).center_location.position + (0, -1, 0)
    ):
        Cylinder(pin_radius, H, align=align.BACK)

    Hole(hole_radius)
    max_fillet = t_hinge.part.max_fillet(
        t_hinge.edges().filter_by(Axis.Z), tolerance=0.2, max_iterations=20
    )
    fillet(objects=t_hinge.edges().filter_by(Axis.Z), radius=max_fillet)

with BuildPart() as shackle:
    with Locations((-2, 0, 0)):
        bla = Box(10, W1, H, align = align.LEFT)
    with Locations(bla.faces().filter_by(Axis.X)[-1].center_location.position):
        bla = Box(14, W1, H, align = align.LEFT)
        Box(80,30,H3,align = align.RIGHT, mode = Mode.SUBTRACT)
    cyl = Cylinder(pin_radius, H, align = align.LEFT)
    with Locations(bla.faces().filter_by(Axis.X)[-1].center_location.position):
        bla = Box(8, W1, H2, align = align.LEFT)
    with Locations(
        bla.faces().filter_by(Axis.X)[-1].center_location.position + (-1, 0, 0)
    ):
        Cylinder(pin_radius, H, align = align.RIGHT)
    max_fillet = shackle.part.max_fillet(
        shackle.edges().filter_by(Axis.Z), tolerance = 2, max_iterations = 20
    )
    fillet(objects=shackle.edges().filter_by(Axis.Z), radius=max_fillet)

j1 = RevoluteJoint(label="t_hinge_hole", to_part=t_hinge.part)
j2 = RigidJoint(
    label="shackle_pin", to_part=shackle.part, joint_location=Location(cyl.center())
)
j1.connect_to(j2, angle = 90)

del align.LEFT, align.RIGHT, bla, cyl, j1, j2

shackle.part.color = "red"

show_all(reset_camera=Camera.KEEP)

comp_hinge_arms = Compound((t_hinge.part, shackle.part))
export_step(comp_hinge_arms, "hinge_lever.step")
