from math import sqrt, asin, pi

from build123d import (
    Align,
    Box,
    Cylinder,
    Line,
    Location,
    Part,
    Vector,
    export_step,
)
from ocp_vscode import Camera, set_port, show_all


# Constants
PHI = (1 + sqrt(5)) / 2
R_OUT = 4.5 / 2
R_IN = 3.2 / 2
CYLINDER_LENGTH = 10
OFFSET = 3.6
OFFSET_LOCATION = Location((0, 0, OFFSET))
BOTTOM_ALIGN = (Align.CENTER, Align.CENTER, Align.MIN)
FLOOR_OFFSET = Location((0, 0, 5.9))
angle_xob = asin(1 / sqrt(PHI**2 + 1)) * (180 / pi)

# Icosahedron vertices
icosahedron_vertices = (
    [Vector(0, i, j * PHI) for i in [-1, 1] for j in [-1, 1]]
    + [Vector(i, j * PHI, 0) for i in [-1, 1] for j in [-1, 1]]
    + [Vector(i * PHI, 0, j) for i in [-1, 1] for j in [-1, 1]]
)

# Axes from the first vertex
axes = [
    Line(icosahedron_vertices[0], icosahedron_vertices[i]).to_axis()
    for i in range(2, 12, 2)
]
additional_axis = Line(icosahedron_vertices[0], icosahedron_vertices[3]).to_axis()


# Function to create a hollow cylinder along a plane
def create_hollow_cylinder(line):
    return line.to_plane() * (
        Cylinder(R_OUT, CYLINDER_LENGTH, align=BOTTOM_ALIGN)
        - OFFSET_LOCATION * Cylinder(R_IN, CYLINDER_LENGTH - OFFSET, align=BOTTOM_ALIGN)
    )


icosahedron_joint: Part = Part()

# Add hollow cylinders along primary axes
for axis in axes:
    icosahedron_joint += create_hollow_cylinder(axis)

# Add additional features
icosahedron_joint += additional_axis.to_plane() * Cylinder(1.3, 3.83)
icosahedron_joint -= (
    additional_axis.to_plane() * FLOOR_OFFSET * Box(20, 20, 4, align=BOTTOM_ALIGN)
)
icosahedron_joint.locate(Location((0, 0, 0), (angle_xob, 0, 0)))

# Visualization
if __name__ == "__main__":
    set_port(3939)
    show_all(reset_camera=Camera.KEEP)
    export_step(icosahedron_joint, "icosahedron_joint.step")
