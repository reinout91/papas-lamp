from build123d import (
    Axis,
    Cylinder,
    Face,
    Line,
    Location,
    Polyline,
    Pos,
    Shell,
    SlotCenterToCenter,
    Solid,
    Spline,
    Vector,
    Wire,
    export_step,
    extrude,
    mirror,
)
from ocp_vscode import Camera, set_port, show_all

b0 = Vector(0, 0, 0)
b1 = Vector(0, 32.8, 0)
b2 = Vector(17.4, 40, 0)
b3 = Vector(36.2, 43.8, 0)
b5 = Vector(28.6, 2, 0)
b6 = Vector(14.3, 0, 0)


base = [b0, b1, b2, b3, b5, b6, b0]

m0 = Vector(0, 0, -13)
m1 = Vector(0, 26.4, -13)
m2 = Vector(15, 30, -17)
m3 = Vector(27.0, 31.5, -13)
m5 = Vector(20.2, 0.5, -13)
m6 = Vector(10.2, 0, -13)


d3 = Vector(31.0, 40, -1.3)
d5 = Vector(24.0, 0, -1.7)

mid = [m0, m1, m2, m3, m5, m6, m0]
o = [(0, 0, -2) + pt for pt in mid[3:5]]
o[0] += (-0.5, -2.5, 0)
o[1] += (-0.5, 0.5, 0)

top = [
    Vector(0, 0, -43),
    Vector(7, 0, -46.5),
    Vector(14, 0, -50),
]

wire1 = Wire(Polyline(b0, m0, m1, b1, b0))

s1 = Spline([b3, Vector(28.57, 36.87, -5.54), o[0]])
s2 = Spline([o[1], Vector(21.75, -0.08, -5.68), b5])
s3 = Spline([top[1], Vector(12, 21, -27.6), m2])
s4 = Spline([top[2], Vector(21.8, 15.8, -34.6), o[0]])
s5 = Spline([top[0], Vector(0, 19.25, -23.7), m1])

wire3 = Wire(
    [
        s1,
        Line(o[0], o[1]),
        s2,
        Line(b5, b3),
    ]
)

wire4 = Wire([Line([m0, top[0]]), s5, Line(m1, m0)])


wire6 = Wire(
    [
        Line([o[1], top[2]]),
        s4,
        Line(o[0], o[1]),
    ]
)

wire8 = Wire(Polyline([o[1], top[2]], top[1], m6, o[1]))
wire9 = Wire(Polyline([m6, top[1], top[0], m0, m6]))
wire10 = Wire([s2, Line(b5, b6), Line(b6, m6), Line(m6, o[1])])
wire11 = Wire(Polyline(b0, m0, m6, b6, b0))
wire12 = Wire(Polyline(b1, m1, m2, b2, b1))
wire13 = Wire(Polyline(b0, b1, b2, b6, b0))
wire14 = Wire(Polyline(b6, b2, b3, b5, b6))
wire15 = Wire([Line(b2, m2), Line(m2, o[0]), s1, Line(b3, b2)])
wire16 = Wire(
    [
        Line(top[0], top[1]),
        s3,
        Line(m2, m1),
        s5,
    ]
)
wire17 = Wire(
    [
        Line(top[2], top[1]),
        s3,
        Line(m2, o[0]),
        s4,
    ]
)

solid = (
    Solid(
        Shell(
            [
                Face.make_surface(wire)
                for wire in [
                    wire1,
                    wire3,
                    wire4,
                    wire6,
                    wire8,
                    wire9,
                    wire10,
                    wire11,
                    wire12,
                    wire13,
                    wire14,
                    wire15,
                    wire16,
                    wire17,
                ]
            ]
        )
    )
    - Location((20, 5.4, -19 - 15), (0, 90, 0))
    * extrude(SlotCenterToCenter(center_separation=30, height=10.8), 8.6, both=True)
    - Location((14.5, 5.4, 0)) * (Cylinder(4.2 / 2, 60) + Cylinder(12.2 / 2, 23))
)


if __name__ == "__main__":
    export_step(solid.rotate(Axis.X, 180), "insert.step")
    export_step(mirror(solid).rotate(Axis.X, 180), "insert_left.step")

    set_port(3939)
    show_all(reset_camera=Camera.KEEP)
