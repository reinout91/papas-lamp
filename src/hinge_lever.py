import copy
from typing import Union

import build123d
from build123d import *
from build123d.topology import tuplify
from ocp_vscode import *

set_port(3939)

print(build123d.__version__)


#specify parameters on base of the hinges
H=6*MM #height of the hinge lever. has to be larger than rad_H.
pin_L=6*MM #length of the pin of all levers. (handy for printing to keep the same as H)
B=3*MM #thickness of the hinge lever with 0.2 margin.
rad_H=1.8*MM #radius of the hinge pin with 0.1 margin (times 2 for diameter).
tol=0.3*MM #a tollerance between rotating parts. has to be smaller than all other parameters.
tol_arm=1.5*MM #tollerance of the arms to the rotation point.
arm2base_L=60*MM #length of the first arm
arm2outer_ring_L=20*MM #length of the second arm

with BuildPart () as arm2base:
    Box(H,arm2base_L,pin_L)

    #making snap fingers at the end of the arm.
    with Locations ((0,arm2base_L/2,-pin_L/2),(0,arm2base_L/2,pin_L/2)):
        Box(H,2*rad_H+tol_arm,pin_L-B,
            align=(Align.CENTER,Align.MAX,Align.CENTER),
            mode=Mode.SUBTRACT
        )
    with Locations((0,arm2base_L/2-rad_H-2*tol,0)):
        Cylinder(rad_H, pin_L,
                 )


    #join the other arm with an inner pin hinge
    with Locations ((H/2,0,0)):
        Box(rad_H*2+tol_arm+2*tol,H,B-tol/2,
            align=(Align.MIN, Align.CENTER, Align.CENTER),
            )
    with Locations((H/2+tol_arm,0,0)):
        Cylinder(rad_H,
                 pin_L,
                 rotation=(0,0,0),
                 align=(Align.MIN, Align.CENTER, Align.CENTER),
                 mode=Mode.SUBTRACT
                 )

    fillet(objects=arm2base.edges().filter_by(Axis.Z),radius=rad_H+tol)



with BuildPart () as arm2outer_ring:
    with Locations ((H/2+2*rad_H+2*tol_arm,0,0)):
        Box(arm2outer_ring_L,H,pin_L,
            align=(Align.MIN, Align.CENTER, Align.CENTER)
            )

    #making snap fingers at the end of the arm
    with Locations ((arm2outer_ring_L+H/2+2*rad_H+2*tol_arm,0,-pin_L/2),(arm2outer_ring_L+H/2+2*rad_H+2*tol_arm,0,pin_L/2)):
        Box(2*rad_H+tol_arm,H,pin_L-B,
            align=(Align.MAX,Align.CENTER,Align.CENTER),
            mode=Mode.SUBTRACT
        )
    with Locations((arm2outer_ring_L+H/2+2*rad_H+2*tol_arm-rad_H-2*tol,0,0)):
        Cylinder(rad_H, pin_L,
                 )


    #join the other arm with an inner pin hinge
    with Locations ((H/2+tol_arm,0,-pin_L/2+(pin_L-B-tol)/4),(H/2+tol_arm,0,pin_L/2-(pin_L-B-tol)/4)):
         Box(2*rad_H+tol_arm,H,(pin_L/2-(B+tol)/2),
             align=(Align.MIN,Align.CENTER,Align.CENTER)
             )
    with Locations ((H/2+tol_arm+tol,0,0)):
        Cylinder(rad_H-tol,
                 pin_L,
                 rotation=(0,0,0),
                 align=(Align.MIN, Align.CENTER, Align.CENTER),
                 )
    fillet(objects=arm2outer_ring.edges().filter_by(Axis.Z), radius=rad_H+tol)


comp_hinge_arms=Compound((arm2base.part,arm2outer_ring.part))

show_all(reset_camera=Camera.KEEP)

comp_hinge_arms.export_step("hinge_lever.step")