
import copy
from typing import Union

import build123d
from build123d import *
from build123d.topology import tuplify
from ocp_vscode import *

set_port(3939)

print(build123d.__version__)

n_sides=7
g = 5.3





with BuildPart() as outer_ring:
    #maak een ring waarin je schroefdraad kan plaatsen met daarom heen een torus die kan gebruikt worden als slider.
    Cylinder(6.0, 2, align=(Align.CENTER, Align.CENTER, Align.CENTER))
    Cylinder(5.0, 5, align=(Align.CENTER, Align.CENTER, Align.CENTER))
    Cylinder(4.5, 5, align=(Align.CENTER, Align.CENTER, Align.CENTER), mode = Mode.SUBTRACT)
    #!!!HELIX MOET NOG GEPLAATST, maar beetje zonde om die 2x te defineren..

with BuildPart() as hinge_base:
    Cylinder(6.5, 5)

    #maak onderdelen aan de slider waar vervolgens weer een scharnier in geplaatst kan worden.
    with PolarLocations(radius=g, count=n_sides, start_angle=360 / (2 * n_sides)):
        with Locations((0, 1, 0), (0, -1, 0)):
            Box(6, 1, 5, align=(Align.MIN, Align.CENTER, Align.CENTER))

        with Locations((4, 0, 0)):
            Cylinder(
                1,3,360,(90, 0, 0),
                (Align.CENTER, Align.CENTER, Align.CENTER),
                Mode.SUBTRACT,
            )

    Cylinder(6.1, 2.1, mode=Mode.SUBTRACT)
    Cylinder(5.1, 5, mode=Mode.SUBTRACT)

    #fillet(hinge_base.edges().filter_by(Plane.XY),radius=0.1)


show_all(reset_camera=Camera.KEEP)