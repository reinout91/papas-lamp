from build123d import MM, Box, BuildPart, Cylinder, Face, GeomType, Hole, Locations
from build123d import (
    __version__ as vs,
)
from build123d_ease import (
    align,
    front_face_of,
)
from ocp_vscode import Camera, set_port, show_all

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

print(vs)

# Build the hinge part
with BuildPart() as t_hinge:
    Cylinder(pin_radius, H, align=align.ANCHOR_CENTER)

    with Locations((0, W1 / 2, 0)):
        ref1 = Box(W1, length_snapfinger, H2, align=align.ANCHOR_BACK)

    with Locations((0, -axle_to_axle, 0)):
        Box(hole_x + 3, W1, H2, align=align.ANCHOR_LEFT)
        with Locations((hole_x, 0, 0)):
            Hole(hole_radius)

    with Locations(front_face_of(ref1)):
        ref2 = Box(H, W1, length_thinge, align=align.ANCHOR_BOTTOM)

c: list[Face] = [
    face
    for face in t_hinge.part.faces().filter_by(GeomType.CYLINDER)
    if any(edge.is_closed for edge in face.edges())
]
[print(face.normal_at(0, 0)) for face in c]
[print(face.normal_at(1, 1)) for face in c]
[print(face.normal_at(0.5, 0.5)) for face in c]

set_port(3939)
show_all(reset_camera=Camera.KEEP)
