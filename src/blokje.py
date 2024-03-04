from build123d import *
from ocp_vscode import *
set_port(3939)

# In Builder mode
with BuildPart() as box1_builder:
    Box(10, 10, 10)
    box2 = Box(5, 5, 5, mode=Mode.PRIVATE)  # for construction only
    box2_top_plane = Plane(box2.faces().sort_by(Axis.Z)[-1])  # plane made from box2 top
    split(bisect_by=box2_top_plane, keep=Keep.TOP)  # split and keep the top

box1 = box1_builder.part
show_all()
show_object(box1)
#input()

# In Algebra mode
#box1 = split(Box(10, 10, 10), Plane(Box(5, 5, 5).faces().sort_by(Axis.Z)[-1]))
