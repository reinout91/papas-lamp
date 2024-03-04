from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
set_port(3939)

from build123d import *
result = SlotOverall(2.625*2, 1.5*2, align=(Align.CENTER, Align.MIN))
result += Pos(Y=1.5) * Rectangle(1.5*2, 4-1.5, align = (Align.CENTER, Align.MIN))
result = split (result, Plane.YZ, keep = Keep.BOTTOM)
result = fillet(result.vertices().sort_by(Axis.Y)[-3], 0.75)
result -= Pos(-2.625+1.5, 1.5) * Circle(0.5/2)
result = Plane.YZ.offset(5/2) * extrude(result, -0.25)
result += result.mirror(Plane.YZ)
base = extrude(Rectangle(5,4, align = (Align.CENTER, Align.MIN)), 0.25)
result += Plane.XZ * base
show_object(result)

