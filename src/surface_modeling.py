from build123d import *

from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
set_port(3939)
with BuildPart() as p:
    with BuildSketch() as s:
        SlotCenterPoint((0,0),(-6,0),5)
        with Locations((-6,0)):
            Circle(1,mode=Mode.SUBTRACT)
    extrude(amount=.5,both=True)
    split(bisect_by=Plane.YZ.offset(-3),keep=Keep.BOTTOM)

    with Locations((Plane.XZ.offset(0))):
        with Locations(Rotation(0,180,0)):
            add(p.part)

    f1 = p.faces().filter_by(Axis.X).sort_by(Axis.X)[0]
    f2 = p.faces().filter_by(Axis.X).sort_by(Axis.X)[-1]

    f1v1 = f1.vertices()[0]
    f2v1 = f2.vertices()[1]

    with BuildLine() as l0:
        Spline(Vector(f1v1),Vector(f2v1),tangents=[(1,0),(1,0)])

    f1v1 = f1.vertices()[1]
    f2v1 = f2.vertices()[0]

    with BuildLine() as l1:
        Spline(Vector(f1v1),Vector(f2v1),tangents=[(1,0),(1,0)])

    f1v1 = f1.vertices()[2]
    f2v1 = f2.vertices()[3]

    with BuildLine() as l2:
        Spline(Vector(f1v1),Vector(f2v1),tangents=[(1,0),(1,0)])

    f1v1 = f1.vertices()[3]
    f2v1 = f2.vertices()[2]

    with BuildLine() as l3:
        Spline(Vector(f1v1),Vector(f2v1),tangents=[(1,0),(1,0)])

r1 = Face.make_surface_from_curves(l0.line.edge(),l1.line.edge())
r2 = Face.make_surface_from_curves(l1.line.edge(),l2.line.edge())
r3 = Face.make_surface_from_curves(l2.line.edge(),l3.line.edge())
r4 = Face.make_surface_from_curves(l3.line.edge(),l0.line.edge())

s1 = Shell([r1,r2,r3,r4,f1,f2])

final = p.part + Solid(s1)


show_object(final)