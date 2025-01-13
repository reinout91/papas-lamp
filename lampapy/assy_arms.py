import copy
from enum import Enum, auto

from assy_leaf import CylinderType, get_cylindric_faces_and_axes

# from assy_leaf import assy_leaf
from build123d import (
    Axis,
    Compound,
    ShapeList,
    Location,
    add,
    Locations,
    Cylinder,
    Vector,
    PolarLocations,
    Box,
    BuildPart,
    Align,
    PositionMode,
    FrameMethod,
    Line,
    Plane,
)
from hexacon_pin import hexacon_pin
from ocp_vscode import Camera, set_port, show_all
from utils import axis_from_three_points, polar_locations_from_rectangular_locations

# AttributeError: 'list' object has no attribute 'values'
# centre = 0.5 * sum(surface.position_at(i, 0.5) for i in [0, 0.5])

grouped_shapes = ShapeList(
    [
        # extract the axis
        tup[1]
        for tup in get_cylindric_faces_and_axes(
            hexacon_pin.part, cylinder_type=CylinderType.HOLE
        )
    ]
).group_by(lambda f: (f.direction.X, f.direction.Y, f.direction.Z))
pts = [Vector(0.5 * (pair[0].position + pair[1].position)) for pair in grouped_shapes]


central_axis = axis_from_three_points(pts)

a = polar_locations_from_rectangular_locations(pts, central_axis)


if __name__ == "__main__":
    set_port(3939)
    show_all(reset_camera=Camera.KEEP)
