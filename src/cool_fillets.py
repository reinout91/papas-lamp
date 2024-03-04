import build123d as bd
import ocp_vscode as view
from typing import List


edgeCoulours = (
    "red",
    "green",
    "blue",
    "yellow",
    "orange",
    "purple",
    "pink",
    "cyan",
    "magenta",
    "brown",
    "grey",
    "white",
)


def show_edges(edges: List[bd.Edge]):
    count = 0
    for edge in edges:
        colour = edgeCoulours[count % len(edgeCoulours)]
        edge.label = f"edge_{count}_{colour}"
        view.show_object(edge, options={"color": colour})
        count += 1


part = bd.Part()
part += bd.Cylinder(5, 10)
part += bd.Plane.YZ * bd.Pos(0, 2, 5) * bd.Cylinder(2, 10)

pipe_intersection = part.edges().group_by(bd.Axis.Z)

show_edges(pipe_intersection)
part = bd.fillet(pipe_intersection[2], 4)


view.show_object(part)