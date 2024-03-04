from build123d import *
from ocp_vscode import *

top = 8
bottom = 12
height = 6
with BuildPart() as bp:
    with BuildSketch():
        Rectangle(bottom, top)
    with BuildSketch(Plane.XY.offset(height)):
        Rectangle(top, top)
    l = loft()
    add(l, rotation=(0, 0, 90))
    with GridLocations(top, top, 2, 2):
        Cone(
            (bottom - top) / 2, 0, height, align=(Align.CENTER, Align.CENTER, Align.MIN)
        )

        
show_object(bp)
