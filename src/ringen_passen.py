from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
from build123d import *
from math import pi
set_port(3939)

pip_count = 3

max_ringmaat = 90 * MM
min_ringmaat = 48 * MM
hoogte_ring = 3 * MM
ring_dikte = 1 * MM

#ring miriam: size 17mm, thickness, 1.2 of 1.4, height: 3mm

sizes = [19, 19.25, 19.8]*MM
radii = [i / 2 for i in sizes]
thicknesses = [1.2, 1.4, 1.6]*MM
height = [3] * MM

spacing = 20+2*max(thicknesses)
distance2 = max(radii)
zspace = 80

with BuildPart() as ringen:
    for zi, h in enumerate(height):
        with BuildSketch() as plan:
            for xi, i in enumerate(radii):
                for yi, j in enumerate(thicknesses):
                    if h == 2:
                        xpos = zi*zspace + xi*(spacing+distance2)
                        ypos = yi*(spacing+distance2)
                    else:
                        xpos = 160 - zi*zspace + xi*(spacing+distance2)
                        ypos = 140 + yi*(spacing+distance2) 
                    with Locations((xpos, ypos)):   
                        Circle(radius=(i+j))          
                        Circle(radius=i, mode=Mode.SUBTRACT)
        extrude(amount = h)
        fillet(
            ringen.edges()
            .filter_by(GeomType.CIRCLE),
            radius=0.59)
show_object(ringen)
ringen.part.export_step("ringen_groot3.step")