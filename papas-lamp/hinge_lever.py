import copy
from typing import Union

import build123d
from build123d import *
from build123d.topology import tuplify
from ocp_vscode import *
from build123d_ease import align, back_face_of, front_face_of

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

hole_x = 10 * MM
axle_to_axle = 30 * MM

with BuildPart() as t_hinge:
    Cylinder(pin_radius, H, align=align.CENTER)
    with Locations((0, -axle_to_axle, 0)):
        Box(hole_x+3, W1, H2, align = align.LEFT)
        with Locations((hole_x, 0, 0)):
            hole = Hole(hole_radius)
    with Locations((0,-1,0)):
        ref1 = Box(W1, 8, H2, align=align.CENTER)
    with Locations(front_face_of(ref1)):
        ref2 = Box(H,  W1, 50, align = align.BOTTOM)
    max_fillet = t_hinge.part.max_fillet(
        t_hinge.edges().filter_by(Axis.Z), tolerance=0.2, max_iterations=20
    )
    fillet(objects=t_hinge.edges().filter_by(Axis.Z), radius=max_fillet)

with BuildPart() as shackle:

    dist1 = axle_to_axle/2
    dist2 = 2.2
    with BuildSketch():
        SlotCenterToCenter(dist1,6)
    ex28_ex = extrude(amount=2*(H2-H3), both=True, mode = Mode.PRIVATE)
    with Locations((dist1/2,0,0)):
        with Locations((0,0,-dist2), (0,0,dist2)):
            add(ex28_ex)
    del ex28_ex
    cyl = Cylinder(pin_radius, H3, align = align.CENTER, mode=Mode.ADD)

    wp = Plane(origin=(dist1+(dist1/2),0,0))

    with BuildSketch(wp):
        SlotCenterToCenter(dist1,6)
    extrude(amount=1.4, both=True, mode = Mode.ADD)
    with Locations((axle_to_axle,0,0)):
        Cylinder(pin_radius, 6, align = align.CENTER, mode=Mode.ADD)

j1 = RevoluteJoint(label="t_hinge_hole", to_part=t_hinge.part, axis= Axis(hole.center(),(0,0,1)))
j2 = RigidJoint(
    label="shackle_pin", to_part=shackle.part, joint_location=Location(cyl.center())
)
j1.connect_to(j2, angle = 90)

del cyl, j1, j2, hole, ref1, ref2

shackle.part.color = "red"

show_all(reset_camera=Camera.KEEP)

comp_hinge_arms = Compound((t_hinge.part, shackle.part))
export_step(comp_hinge_arms, "hinge_lever.step")
