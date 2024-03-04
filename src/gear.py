from build123d import *
from ocp_vscode import *
densc = 1020 / 1e6  # ABS
with BuildPart() as p:
    with BuildSketch() as s:
        with PolarLocations(0,10):
            Circle(6/2)
            with Locations((5.75/2,0)):
                Circle(.5)
    extrude(amount=1.75)
    with PolarLocations(5.75/2,10):
        Hole(.5/2)
    with BuildSketch() as s:
        Circle(4.5/2)
    extrude(amount=-3.25+1.75)
    with Locations((Plane.XY.offset(1.75))):
        CounterSinkHole(3.75/2,4.75/2,counter_sink_angle=70)

print(f"\npart mass = {p.part.scale(IN).volume/LB*densc}")

show_object(p)
