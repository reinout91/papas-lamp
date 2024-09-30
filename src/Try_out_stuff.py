'''
26--05-2024
Miriam is trying build123. Miriam wants to make a lamp for Reinout.
'''

from ocp_vscode import Camera, set_port, show, show_all

set_port(3939)
from typing import Union

from build123d import *
from build123d.build_common import validate_inputs
from build123d.topology import Solid, tuplify

'''
with BuildPart() as hinge_base:
    with Locations((0,1,0),(0,-1,0)):
        Box(4,1,5, align = (Align.MAX, Align.CENTER, Align.MIN))
    with Locations((-1,0,3)):
        Cylinder(radius=1, height=3, rotation=(90, 0, 0), align = (Align.MAX, Align.CENTER, Align.CENTER), mode=Mode.SUBTRACT)

    #making a joint
    RigidJoint(label = "hinge_base_rigid", #to_part = pinpart.part,
               joint_location= Location((-2,0,3),(90,0,0))) #adding a orientation doesn't seems to do anything
    print(hinge_base.location)

# build the hinge pin part
with BuildPart() as pinpart:
    (L, H, B)= (2,10,2)
    pts = [
    (-2, -2),
    (B, -2),
    (B, H),
    (-2, H+2),
    ]
    with BuildSketch(Plane.YZ) as beam2:
        with BuildLine():
            t = Polyline(*pts, close= True)
        make_face()  # Create a filled 2D shape
    extrude(amount=0.4,both=True)

    with Locations((0,0,0)):
        Cylinder(radius=0.9, height=3, rotation=(0,90,0), align = (Align.CENTER, Align.CENTER, Align.CENTER), mode=Mode.ADD)

    #making a joint, define the axis by a location and a direction to pivot.
    RevoluteJoint(label="pinpart_hinge_joint",axis=Axis((0,0,0),(1,0,0)))
    print(pinpart.location)

#connecting the joints
hinge_base.part.joints["hinge_base_rigid"].connect_to(pinpart.part.joints["pinpart_hinge_joint"],
                                                      angle=180) #code base, why the inverse?
'''
with BuildPart() as testwedgde:
    Wedge(0.1, 1, 1, 0.3, 0, 2, 5)

'''
class HelixShape(BasePartObject):

    # _applies_to = [BuildPart._tag]

    def __init__(
        self,
        heigth: float,
        length: float,
        radius: float,
        threadradius: float,
        rotation: RotationLike = (0, 0, 0),
        align: Union[Align, tuple[Align, Align, Align]] = (
            Align.CENTER,
            Align.CENTER,
            Align.CENTER,
        ),
        mode: Mode = Mode.ADD,
    ):
        context: BuildPart = BuildPart._get_context(self)
        validate_inputs(context, self)

        # self.length = length
        # self.width = width
        # self.box_height = height
        with BuildPart() as p:
            with BuildLine ():
                l1 = Helix(3,30,5.2)
            with BuildSketch(Plane(origin=l1 @ 0, z_dir=l1 % 0)) as example_7_section:
                Circle(threadradius)
            sweep()

        solid = p.part.solid()

        super().__init__(
            part=solid, rotation=rotation, align=tuplify(align, 3), mode=mode
        )

# class Innerhelix(BasePartObject):
#     def __init__(self, mode=Mode.ADD):

#         # Cylinder(6,400)
#         Solid.make_cylinder(plane=Plane(0,0,1), height=6, radius=60)

#         super().__init__(part=solid, rotation=(0, 0, 0), mode=mode)


with BuildPart() as Outer_Tube:
    with Locations((0,0,60/2)):
        Cylinder(6,30)
        Hole(5.1)
        HelixShape(10,10, threadradius = 0.2, mode=Mode.SUBTRACT)
        # Box(10,10,10)

        # with Locations((0,0,30/2)):
        #     Cylinder(5,30)
        #     Hole(4.8)'''




#visualisation
# Outer_Tube.color=Color("red")
show_all(reset_camera=Camera.KEEP, render_joints = True, render_mates = True)
