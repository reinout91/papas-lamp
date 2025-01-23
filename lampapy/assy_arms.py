import copy

from assy_leaf import CylinderType, assy_leaf, get_cylindric_faces_and_axes
from build123d import (
    Axis,
    Compound,
    RevoluteJoint,
    RigidJoint,
    Rot,
    ShapeList,
    Vector,
)
from hexacon_pin import hexacon_pin
from ocp_vscode import Camera, set_port, show_all
from utils import axis_from_three_points, polar_locations_from_rectangular_locations

grouped_shapes = ShapeList(
    [
        tup[1]
        for tup in get_cylindric_faces_and_axes(
            hexacon_pin.part, cylinder_type=CylinderType.HOLE
        )
    ]
).group_by(lambda f: (f.direction.X, f.direction.Y, f.direction.Z))

pts = [Vector(0.5 * (pair[0].position + pair[1].position)) for pair in grouped_shapes]

central_axis = axis_from_three_points(pts)
polar_locations = polar_locations_from_rectangular_locations(pts, central_axis)

rigid_joints = [
    RigidJoint(
        label="hoi", to_part=hexacon_pin.part, joint_location=loc * Rot((-90, 0, 0))
    )
    for loc in polar_locations
]


instances: list[Compound] = [copy.copy(assy_leaf) for loc in polar_locations]
rev_joints = [
    RevoluteJoint(label="assy_leaf", to_part=p, axis=Axis.Z) for p in instances
]
for i, j in enumerate(rigid_joints):
    j.connect_to(rev_joints[i], angle=50)

del assy_leaf
if __name__ == "__main__":
    set_port(3939)
    show_all(reset_camera=Camera.KEEP)
