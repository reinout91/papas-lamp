import copy
from enum import Enum, auto

# from assy_leaf import assy_leaf
from build123d import Compound, ShapeList, Axis
from hexacon_pin import hexacon_pin
from ocp_vscode import Camera, set_port, show_all
from assy_leaf import get_cylindric_faces_and_axes, CylinderType

# AttributeError: 'list' object has no attribute 'values'
# centre = 0.5 * sum(surface.position_at(i, 0.5) for i in [0, 0.5])

grouped_shapes = ShapeList(
    get_cylindric_faces_and_axes(hexacon_pin.part, cylinder_type=CylinderType.HOLE)
).group_by(lambda f: f[1])
# sumlocation) / 1 .. group_by(axis.direction)
print(aap.group_by)
# assy_arms = Compound(hexacon_pin.part, joints=hexacon_pin.joints)

if __name__ == "__main__":
    set_port(3939)
    show_all(reset_camera=Camera.KEEP)
