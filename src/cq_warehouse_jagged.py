from build123d import *
from ocp_vscode import *
import cadquery as cq
import cq_warehouse.extensions
polygon_box_faces = (
    cq.Workplane()
    .rect(216, 76)
    .extrude(25)
    .edges("not >Z")
    .makeFingerJoints(
        materialThickness=3,
        targetFingerWidth=6,
        kerfWidth=-0.1,
    )
)
box_face_bottom = polygon_box_faces.faces("<<Z")
b3d_polygon_box_face = Solid.make_box(1,1,1).faces().sort_by(Axis.Z)[-1]
b3d_polygon_box_face.wrapped = box_face_bottom.val().wrapped
with BuildSketch() as bs1:
    add(b3d_polygon_box_face)
    Circle(5, mode=Mode.SUBTRACT)
show(bs1)