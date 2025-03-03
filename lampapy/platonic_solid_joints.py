from math import acos, asin, atan, pi, sqrt

from build123d import (
    Align,
    Axis,
    Cylinder,
    Line,
    Location,
    Part,
    Vector,
    export_step,
    objects_part,
)
from ocp_vscode import Camera, set_port, show_all

PHI = (1 + sqrt(5)) / 2
R_OUT = 4.5 / 2
R_IN = 3.2 / 2
CYLINDER_LENGTH = 10
OFFSET = 3.6
OFFSET_LOCATION = Location((0, 0, OFFSET))
BOTTOM_ALIGN = (Align.CENTER, Align.CENTER, Align.MIN)

ICOSAHEDRON_XOB = asin(1 / sqrt(PHI**2 + 1)) * (180 / pi)
DODECAHEDERON_XOB = acos(-(sqrt(3) + sqrt(15)) / 6) * (180 / pi) - 180
TETRAHEDRON_AND_CUBE_XOB = atan(sqrt(2)) * 180 / pi


def create_hollow_cylinder(
    axis: Axis, rotation: tuple[float, float, float]
) -> objects_part:
    return axis.to_plane() * (
        Cylinder(R_OUT, CYLINDER_LENGTH, align=BOTTOM_ALIGN, rotation=rotation)
        - OFFSET_LOCATION
        * Cylinder(
            R_IN, CYLINDER_LENGTH - OFFSET, align=BOTTOM_ALIGN, rotation=rotation
        )
    )


# %% OCTAHEDRON
octahedron_joint: Part = Part(label="octahedron_joint")
octahedron_vertices = (
    [Vector(i, 0, 0) for i in [-1, 1]]
    + [Vector(0, i, 0) for i in [-1, 1]]
    + [Vector(0, 0, i) for i in [-1, 1]]
)

top_vertex_octahedron_joint = 5
axes_octahedron_joint = [
    Line(
        octahedron_vertices[top_vertex_octahedron_joint], octahedron_vertices[i]
    ).to_axis()
    for i in (0, 1, 2, 3)
]

for axis in axes_octahedron_joint:
    octahedron_joint += create_hollow_cylinder(axis, rotation=(0, 0, 30.0)) + Location(
        (0, 0, 1.93)
    ) * Cylinder(1.9, 1.4)

# %% CUBE
cube_joint: Part = Part(label="cube_joint")
cube_vertices = [
    vert.rotate(Axis((0, 0, 0), (1, 1, 0)), TETRAHEDRON_AND_CUBE_XOB)
    for vert in (Vector(i, j, k) for i in [-1, 1] for j in [-1, 1] for k in [-1, 1])
]

top_vertex_cube = 3
axes_cube_joint = [
    Line(cube_vertices[top_vertex_cube], cube_vertices[i]).to_axis() for i in (1, 2, 7)
]

for axis in axes_cube_joint:
    cube_joint += create_hollow_cylinder(axis, rotation=(0, 0, 30.0)) + Location(
        (0, 0, 1.93)
    ) * Cylinder(1.9, 4)

# %% TETRAHEDRON
tetrahedron_joint: Part = Part(label="tetrahedron_joint")
tetrahedron_vertices = [
    vert.rotate(Axis((0, 0, 0), (1, -1, 0)), TETRAHEDRON_AND_CUBE_XOB)
    for vert in (
        Vector(1, 1, 1),
        Vector(1, -1, -1),
        Vector(-1, 1, -1),
        Vector(-1, -1, 1),
    )
]

top_vertex_tetrahedron = 0
axes_tetrahedron_joint = [
    Line(tetrahedron_vertices[0], tetrahedron_vertices[i]).to_axis() for i in (1, 2, 3)
]

for axis in axes_tetrahedron_joint:
    tetrahedron_joint += create_hollow_cylinder(axis, rotation=(0, 0, 30.0)) + Location(
        (0, 0, 1.93)
    ) * Cylinder(1.9, 2.3)


# %% ICOSAHEDRON
icosahedron_joint: Part = Part(label="icosahedron_joint")
icosahedron_vertices = [
    vert.rotate(Axis.X, ICOSAHEDRON_XOB)
    for vert in (
        [Vector(0, i, j * PHI) for i in [-1, 1] for j in [-1, 1]]
        + [Vector(i, j * PHI, 0) for i in [-1, 1] for j in [-1, 1]]
        + [Vector(i * PHI, 0, j) for i in [-1, 1] for j in [-1, 1]]
    )
]

top_vertex_icosahedron = 3
axes_icosahedron_joint = [
    Line(
        icosahedron_vertices[top_vertex_icosahedron], icosahedron_vertices[i]
    ).to_axis()
    for i in range(1, 12, 2)
    if i != top_vertex_icosahedron
]

for axis in axes_icosahedron_joint:
    icosahedron_joint += create_hollow_cylinder(axis, rotation=(0, 0, 30)) + Location(
        (0, 0, 1.93)
    ) * Cylinder(1.3, 4)

# %% DODECAHEDRON
dodecahedron_joint: Part = Part(label="dodecahedron_joint")
dodecahedron_vertices = [
    vert.rotate(Axis.X, DODECAHEDERON_XOB)
    for vert in (
        [Vector(i, j, k) for i in [-1, 1] for j in [-1, 1] for k in [-1, 1]]
        + [Vector(0, i / PHI, j * PHI) for i in [-1, 1] for j in [-1, 1]]
        + [Vector(i / PHI, j * PHI, 0) for i in [-1, 1] for j in [-1, 1]]
        + [Vector(i * PHI, 0, j / PHI) for i in [-1, 1] for j in [-1, 1]]
    )
]

top_vertex_dodecahedron = 9
axes_dodecahedron_joint = [
    Line(
        dodecahedron_vertices[top_vertex_dodecahedron], dodecahedron_vertices[i]
    ).to_axis()
    for i in (1, 5, 11)
]

for axis in axes_dodecahedron_joint:
    dodecahedron_joint += create_hollow_cylinder(
        axis, rotation=(0, 0, 30.0)
    ) + Location((0, 0, 1.93)) * Cylinder(1.3, 4)


if __name__ == "__main__":
    # export results

    platonic_solid_joints = [
        dodecahedron_joint,
        icosahedron_joint,
        tetrahedron_joint,
        cube_joint,
        octahedron_joint,
    ]
    [
        export_step(shape.rotate(Axis.X, 180), f"{shape.label}.step")
        for shape in platonic_solid_joints
    ]

    # Visualization

    # run the server:
    # python -m ocp_vscode

    set_port(3939)
    show_all(
        reset_camera=Camera.KEEP,
    )
