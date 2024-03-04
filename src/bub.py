from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
set_port(3939)

from build123d import *

with BuildPart() as p:
    with BuildSketch(Plane.XY.offset(0)) as s0:
        Circle(0.9213, align=(Align.CENTER, Align.MAX)) # magic number
        with Locations((0, -4)):
            Rectangle(2.5, 0.001)
        make_hull()
    extrude(amount=5.5 / 2)

    with BuildSketch(Plane.YZ.offset(0)) as s:
        Rectangle(4 - 0.25, 4.25, align=(Align.MAX, Align.CENTER))
    extrude(amount=2.5 / 2, both=True, mode=Mode.SUBTRACT)

    with BuildSketch(Plane.XY.offset(4.5 / 2)) as s:
        Circle(0.9213, align=(Align.CENTER, Align.MAX))
    extrude(amount=-0.5)

    with Locations((-Plane.XY.offset(3.5 / 2))):
        with Locations((0, 0.9213)):
            CounterBoreHole(0.625 / 2, 1.25 / 2, 0.5, mode=Mode.SUBTRACT)

    with BuildSketch(Plane.XZ) as s:
        with BuildLine() as l:
            m1 = SagittaArc((-2.5 / 2, 5 / 2), (2.5 / 2, 5 / 2), 0.25)
            m2 = mirror(about=Plane.XZ)
            m3 = Line(m1 @ 0, m2 @ 0)
            m4 = Line(m1 @ 1, m2 @ 1)
        make_face()
    extrude(amount=-8, both=True, mode=Mode.INTERSECT)

    asdf = p.part.edges().filter_by(Axis.X).group_by(Axis.Y)[-1].sort_by(Axis.Z)[-1]
    fillet(asdf, 0.5)
    with BuildSketch() as s:
        with Locations((0, -4 + 0.25)):
            Triangle(A=16 / 2, a=0.5 / 2, B=90, align=(Align.MIN, Align.MIN))
            mirror(about=Plane.YZ)
            fillet(s.vertices().sort_by(Axis.Y)[-1], 0.1257) # magic number
            print(s.sketch.bounding_box().size)
    zz = extrude(amount=2.25)
    mirror(about=Plane.XY)

bb2 = s0.sketch.edges().filter_by(GeomType.CIRCLE, reverse=True).group_by(Axis.Y)[2:4]
print(bb2[0][0].tangent_angle_at(0) - bb2[1][0].tangent_angle_at(0))

show_object(p)