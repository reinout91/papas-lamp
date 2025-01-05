import copy
from typing import Union

import build123d
from build123d import *
from build123d.topology import tuplify
from ocp_vscode import *
from build123d_ease import (
    align, back_face_of, bottom_face_of, front_face_of,
    left_face_of, right_face_of, top_face_of
)

# Parameters for the hinges

W1 = 6 * MM
H = 6 * MM
H3 = 3 * MM  # Height of T joint
H2 = H3
pin_radius = 1.8 * MM
hole_radius = 2 * MM
length_thinge = 50 * MM
length_snapfinger = 7 * MM

hole_x = 10 * MM
axle_to_axle = 20 * MM

print(build123d.__version__)

# Build the hinge part
with BuildPart() as t_hinge:
    Cylinder(pin_radius, H, align=align.CENTER)

    with Locations((0, W1 / 2, 0)):
        ref1 = Box(W1, length_snapfinger, H2, align=align.BACK)

    with Locations((0, -axle_to_axle, 0)):
        Box(hole_x + 3, W1, H2, align=align.LEFT)
        with Locations((hole_x, 0, 0)):
            Hole(hole_radius)

    with Locations(front_face_of(ref1)):
        ref2 = Box(H, W1, length_thinge, align=align.BOTTOM)

c: list[Face] = [face for face in t_hinge.part.faces().filter_by(GeomType.CYLINDER) if any([edge.is_closed for edge in face.edges()])]
[print(face.normal_at(0,0)) for face in c]
[print(face.normal_at(1,1)) for face in c]
[print(face.normal_at(0.5,0.5)) for face in c]

set_port(3939)
show_all(reset_camera=Camera.KEEP)
