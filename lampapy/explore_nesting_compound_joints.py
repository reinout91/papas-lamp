import copy

import build123d as bd
from ocp_vscode import Camera, set_port, show_all

p = (
    bd.Part(None)
    + bd.Box(length=30, width=30, height=30)
    - bd.Cylinder(
        radius=10,
        height=30,
    )
)

p2 = bd.Part(None) + bd.Cylinder(
    radius=8,
    height=50,
)

p_rigid_joint = bd.RigidJoint(label="my_p_joint", to_part=p)

p2_revolute_joint = bd.RevoluteJoint(label="my_p_joint", to_part=p2, axis=bd.Axis.Z)
p_rigid_joint.connect_to(p2_revolute_joint, angle=30)

assy = bd.Compound([p, p2], label="compound")

places = [bd.Location((40, 0, 0)), bd.Location((80, 0, 0))]

instances = [copy.copy(assy) for i in places]

my_joints = [
    bd.RigidJoint(f"place_{i}", to_part=p, joint_location=place)
    for i, place in enumerate(places)
]

my_revolute_joints = [
    bd.RevoluteJoint(f"rev_{i}", to_part=instance, axis=bd.Axis.Z)
    for i, instance in enumerate(instances)
]

[
    my_joints[i].connect_to(my_revolute_joints[i], angle=30)
    for i, _ in enumerate(my_joints)
]


if __name__ == "__main__":
    set_port(3939)
    show_all(reset_camera=Camera.KEEP)
