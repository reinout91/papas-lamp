from build123d import *
from ocp_vscode import *
with BuildPart() as r1:
    with BuildSketch(Plane.XZ) as sk1:
        with Locations((10, 0)):
            Rectangle(5, 1, align=Align.MIN)
        with Locations((12, 0)):
            Rectangle(1, 5, align=Align.MIN)
    revolve()


show_object(r1)