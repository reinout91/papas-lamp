from build123d import *
from ocp_vscode import *

ms = Mode.SUBTRACT
with BuildPart() as p:
    with BuildPart(mode=Mode.PRIVATE) as p0:
        with BuildSketch(Plane.XZ) as s:
            with BuildLine() as l:
                m1 = Line((0,-55/2),(38,-55/2))
                m2 = Line(m1@1,(38,-90/2-10))
                fillet(l.vertices(),8)
                offset(objects=l.line,amount=3,side=Side.LEFT)
            make_face()
        revolve(axis=Axis.X)

        with BuildSketch(Plane.YZ) as s2:
            SlotCenterPoint((0,-55/2),(0,-90/2),20)
        extrude(amount=38,mode=Mode.INTERSECT)

    with BuildSketch() as s3:
        Circle(55/2+3)
        Rectangle(23+6,42,align=(Align.CENTER,Align.MIN))
        Circle(55/2,mode=ms)
        Rectangle(23,42,mode=Mode.SUBTRACT,align=(Align.CENTER,Align.MIN))
        fillet(s3.vertices().group_by(Axis.Y)[0],8)
        fillet(s3.vertices().group_by(Axis.Y)[1],5)
    extrude(amount=-28)
    extrude(s3.sketch,amount=.0001) #hack to prevent OCCT issues
    fillet(p.part.faces().group_by(Axis.Y)[-1].edges().filter_by(Axis.X),7)
    with PolarLocations(0,3,-30):
        with Locations(Rotation((0,90,0))):
            add(p0.part)

    with BuildSketch() as s4:
        with PolarLocations(0,3,0):
            SlotCenterPoint((0,-90/2+2),(0,-90/2),8)
    extrude(amount=-40,mode=ms)

    with BuildSketch(Plane.XY.offset(-28)) as s5:
        with BuildLine() as l:
            n1 = CenterArc((0,0),90/2,-15,-45)
            n2 = Polyline(n1@1,(0,0),n1@0)
        make_face()
    extrude(amount=10,mode=ms)

    zz = p.part.faces().filter_by(Axis.X).sort_by(Axis.X)[-1]
    print(zz.bounding_box().size)
    with BuildSketch(zz) as s6:
        with Locations((12.335206051617345/2-7,2)): #from bbox above
            #position may not be exactly correct, but does not affect the mass
            SlotCenterToCenter(10,5,90)
    extrude(amount=50,both=True,mode=ms)


show_object(p)