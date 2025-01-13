import numpy as np
import build123d as bd
from ocp_vscode import Camera, set_port, show_all, show


def axis_from_three_points(pts: list[bd.VectorLike]) -> bd.Axis:
    arc = bd.Edge.make_three_point_arc(point1=pts[0], point2=pts[1], point3=pts[2])
    center = arc.arc_center
    ax1 = bd.Line(pts[2], center).to_axis()
    ax2 = bd.Axis(center, direction=arc.tangent_at(1))
    ax3 = bd.Axis(center, ax1.direction)
    # Use cross product to get the direction purpendicular to the axes:
    return bd.Axis(center, ax2.direction.cross(ax3.direction))


def polar_locations_from_rectangular_locations(
    pts: list[bd.Location], axis: bd.Axis
) -> list[bd.Location]:
    return [
        bd.Plane(
            pt,
            x_dir=bd.Line(pt, axis.position).to_axis().direction,
            z_dir=axis.direction,
        ).location
        for pt in pts
    ]


if __name__ == "__main__":
    pts = [bd.Vector(0, 0, 9), bd.Vector(2, 0), bd.Vector(4, 5)]
    axis = axis_from_three_points(pts)
    show_all(reset_camera=Camera.KEEP)
