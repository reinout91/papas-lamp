from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
from build123d import *
set_port(3939)

from build123d import *

with BuildPart() as example:
    Cylinder(radius=10, height=3)
    with BuildSketch(example.faces().sort_by(Axis.Z)[-1]):
        RegularPolygon(radius=7, side_count=6)
        Circle(radius=4, mode=Mode.SUBTRACT)
    extrude(amount=-2, mode=Mode.SUBTRACT)

show_object(example)