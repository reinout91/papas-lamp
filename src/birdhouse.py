from build123d import *
from build123d import sqrt
from build123d import floor
from itertools import product
from build123d import sin
from build123d import pi
from numpy import linspace
from enum import Enum, auto
from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
set_port(3939)

def alignment_holes(
    parts: tuple[BuildPart, ...],
    holes: list[Hole]
) -> tuple[BuildPart, ...]:
    return tuple(map(lambda p: p - holes, parts))

# Finger Joint Function
###############################################################
class FingerType(Enum):
    ODD = auto()
    EVEN = auto()

def auto_finger_joint(
        a: Part,
        b: Part,
        min_finger_width: float,
        swap: bool = False,
        finger_type: FingerType = None
    ) -> tuple[Part, Part]:

    # We're operating on the intersection of the two parts
    inter = a.intersect(b)
    edges = inter.edges().copy()
    edges.sort(key=lambda e: e.length, reverse=True)

    # The operation will be along the shortest of the longest 4
    # edges in the direction of the edge
    edge = edges[0]
    z_dir = (edge @ 1 - edge @ 0).normalized()

    # Determine the number of fingers, one is added to the base
    # count since there is technically a 0th cut. That flips some
    # of the even/odd logic 
    n_fingers = floor(edge.length/min_finger_width) + 1
    if finger_type == FingerType.EVEN and not n_fingers & 1:
        n_fingers -= 1
    elif finger_type == FingerType.ODD and n_fingers & 1:
        n_fingers -= 1
    
    # These are the arrays we'll be filling
    fingers_a, fingers_b = [], []

    # We'll use linspace to evenly space the fingers, skip the
    # first and last because they're outside the intersection
    alternate = (fingers_a, fingers_b)
    to_div = inter

    # 1 is added here since 
    for x in linspace(0.0, 1.0, n_fingers)[1:-1]:

        # Split by our plane along the edge
        plane = Plane(origin=edge @ x, z_dir=z_dir)
        divs = [shape for shape in to_div.split(plane, Keep.BOTH)]

        # Select the correct bottom/top
        if plane.to_local_coords(divs[0]).center().Z >= 0:
            alternate[0].append(divs[1])
            to_div = divs[0]
        else:
            alternate[0].append(divs[0])
            to_div = divs[1]

        # Swap the arrays
        alternate = (alternate[1], alternate[0])

    # The remainder will be the last finger
    alternate[0].append(to_div)

    if swap:
        return (a - fingers_b, b - fingers_a)
    else:
        return (a - fingers_a, b - fingers_b)

# Parameters
###############################################################
mat_thicc = 3.35
rad_pull = 8
pull_width = mat_thicc
min_finger_width = 2 * mat_thicc
hlf_thicc = mat_thicc/2
width = 4 * IN # Chickadee
heght = 8 * IN # Chickadee
diam = 1.25 * IN # Chickadee
hole_y = 6 * IN # Chickadee
airationholes = 0.25/2 * IN
roofl = sqrt(2 * (width / 2) ** 2) + mat_thicc
overhang_r = 0
overhang_s = 4 * mat_thicc
overhang_f = 8 * mat_thicc
roofw = width + overhang_r + overhang_f
bracketw = 7 * width/15
slotw = bracketw - 2 * mat_thicc
sloth = heght/2
toothpick = 1.9
align_hole = Hole(toothpick/2, depth=200)


# Roof
###############################################################
roof = Location((0, overhang_s/2)) * Rectangle(roofw, roofl + overhang_s)
roof = fillet(roof.vertices().sort_by(Axis.X)[-2:].sort_by(Axis.Y).last, overhang_f)
roof = Location(
        (
            (overhang_f - overhang_r)/2,
            width/4,
            heght
        ), 
        (-45, 0, 0)
    ) * \
    extrude(roof, mat_thicc/2, both=True)


# Side Panel
#############################################################
side_r = Location((width/4, width/2 - hlf_thicc)) * \
            Rectangle(width/2, mat_thicc)
side = extrude(side_r, until=Until.NEXT, target=roof)

# Front Panel
#############################################################
front_r = Location((width/2 - hlf_thicc, width/4)) * \
            Rectangle(mat_thicc, width/2)
front = extrude(front_r, until=Until.NEXT, target=roof)
front += extrude(
            front.faces().sort_by(Axis.Z).last -
            side.faces().sort_by(Axis.Z).last,
            amount=mat_thicc
        )

# Floor Panel
#############################################################
flr_r =  Rectangle(width/2, width/2)
flr = Location((width/4 - mat_thicc, width/4 - mat_thicc, 2 * mat_thicc)) * extrude(flr_r, amount=mat_thicc)
flr = flr - GridLocations(2 * rad_pull, width/2 + mat_thicc, 2, 2) * Hole(airationholes, 200)

# Finger Joints
#############################################################
(roof, front) = auto_finger_joint(roof, front, min_finger_width, swap=True)
(side, front) = auto_finger_joint(side, front, min_finger_width)


# Mirroring Assemblies
#############################################################
front += mirror(front)
back = mirror(front, about=Plane.ZY)
roof -= back

roof_b = mirror(roof)

flr += mirror(flr)
flr += mirror(flr, about=Plane.ZY)

side += mirror(side, about=Plane.ZY)
side_b = mirror(side)


# Finger Joints 2 Electric Bugaloo
#############################################################
(roof, roof_b) = auto_finger_joint(roof, roof_b, min_finger_width)

# Mounting Bracket
#############################################################
slot = Plane.ZY * (
        Location((sloth, 0)) * Circle(bracketw/2 - mat_thicc) + \
        Location((sloth/2 + 2 * mat_thicc, 0)) * Rectangle(sloth - 2 * mat_thicc, bracketw - 2 * mat_thicc)
    )
slot = Location((-width/2 + mat_thicc, 0)) * extrude(slot, amount=mat_thicc)
bracket_in = Plane.ZY * (
        Location((sloth, 0)) * Circle(bracketw/2) + \
        Location((sloth/2 + 2 * mat_thicc, 0)) * Rectangle(sloth - 2 * mat_thicc, bracketw)
    )
bracket_in = Location((-width/2 + 2 * mat_thicc, 0)) * extrude(bracket_in, mat_thicc)
bracket_out = Plane.ZY * (
        Location((sloth, 0)) * Circle(bracketw/2) + \
        Location((sloth/2, 0)) * Rectangle(sloth, bracketw)
    )
bracket_out = Location((-width/2, 0)) * extrude(bracket_out, mat_thicc)

# Adding cutout for the slot
back -= slot
back -= extrude(slot.faces().sort_by(Axis.Z).first, amount=heght)

mounting_alignments = Plane.ZY * \
    Location((0.75 * slotw, 0)) * \
    PolarLocations(slotw/2, 4, 45) * \
    align_hole

(bracket_in, slot, bracket_out) = alignment_holes(
    (bracket_in, slot, bracket_out),
    mounting_alignments
)

# Extend floor into slot space
flr = flr + extrude(
    Plane(flr.faces().sort_by(Axis.X).first) * Rectangle(slotw, mat_thicc),
    until=Until.NEXT,
    target=bracket_out
)


# Final Hole
#############################################################
front -= Location((0, 0, hole_y), (0, 90, 0)) * Hole(diam/2, depth=500)


# Spring 
#############################################################
rpullw = width - 2 * mat_thicc
rpullh = 3 * mat_thicc
ringoffy = -rad_pull -pull_width + rpullh/2 - mat_thicc
springt = 1.25 * mat_thicc
springw = (rpullw - rpullh)/2
nturns = floor((springw - 1.25 * mat_thicc)/(2 * springt))
springystep = springw/(nturns + 1)

with BuildPart() as spring:
    with BuildSketch() as spring_latch:
        Rectangle(3/5 * rpullw, rpullh)
        with Locations((0, (rpullh - mat_thicc)/2)):
            Rectangle(1/5 * rpullw, mat_thicc, mode=Mode.SUBTRACT)
    extrude(amount=mat_thicc)

    with BuildSketch() as spring_pull:
        with Locations((0, ringoffy)):
            Circle(rad_pull + pull_width)
            with Locations((0, (rad_pull + pull_width)/2)):
                Rectangle((rad_pull + pull_width) * 2, rad_pull + pull_width)
            Circle(rad_pull, mode=Mode.SUBTRACT)
    extrude(amount=mat_thicc)

    fillet(spring.edges(Select.NEW), springt/2)
spring = Location((0, (rpullw - rpullh)/2 + mat_thicc)) * spring.part

spring_path = Line(
    (3/5 * 0.5 * rpullw, (rpullw - springt)/2),
    ((rpullw - springt)/2, (rpullw - springt)/2)
)
springxdir = Vector(-1, 0)
springydir = springystep * Vector(0, -1)

lengths = [
    rpullw/2 - springt - rad_pull - 1.2 * mat_thicc,
    rpullw/2 - springt - rad_pull - 1.2 * mat_thicc,
    rpullw/2 - springt - 0.2 * mat_thicc,
    rpullw/2 - springt - 0.2 * mat_thicc,
]
for (_, l) in zip(range(0, nturns), lengths):
    spring_path = spring_path + Line(spring_path @ 1, spring_path @ 1 + springydir)
    spring_path = spring_path + Line(spring_path @ 1, spring_path @ 1 + l * springxdir)
    springxdir = -springxdir
spring_path = spring_path + Line(spring_path @ 1, spring_path @ 1 + springydir)

spring_path = fillet(spring_path.vertices(), springt)

sweep_rect = Plane(
    origin = (0.5 * 3/5 * rpullw, (rpullw - springt)/2, mat_thicc/2),
    x_dir = Axis.Y.direction,
    z_dir = Axis.X.direction
) * Rectangle(springt, mat_thicc)

spring_path = sweep(sweep_rect, spring_path)

spring = spring + extrude(Rectangle(rpullw, rpullh), amount=mat_thicc) + \
    spring_path + \
    mirror(spring_path, about=Plane.YZ)
spring = fillet(
    spring.edges().filter_by(Axis.Z).sort_by(Axis.Y)[:-10],
    springt/4
)

spring = spring + mirror(spring, about=Plane.XZ)
spring = Location((0, 0, mat_thicc)) * spring

side = side - spring
side_b = side_b - spring

with BuildPart() as floor_holes:
    with GridLocations(3 * rpullw/10, 0, 3, 1):
        with PolarLocations(0.75 * rpullh, 2, 15):
            Cylinder(toothpick/2, 200)
            

(spring, flr) = alignment_holes(
    (spring, flr),
    floor_holes.part
)

# Floor Aligner
################################################################################
flrah = min_finger_width * 3
flr_align = Location(((width - flrah)/2 - mat_thicc, 0, 3 * mat_thicc)) * extrude(
    Rectangle(flrah, width),
    amount=mat_thicc
)
(flr_align, side) = auto_finger_joint(flr_align, side, min_finger_width, True)
(flr_align, side_b) = auto_finger_joint(flr_align, side_b, min_finger_width, True)

show(
    front,
    side,
    side_b,
    roof,
    roof_b,
    flr,
    back,
    bracket_in,
    slot,
    bracket_out,
    flr_align,
    # spring_path,
    spring
)


# DXFS
#############################################################
def save_dxfs(name: str, part: Part, multiface: bool = False):
    
    exporter = ExportDXF()
    faces = part.faces().sort_by(SortBy.AREA)


    if multiface:
        exporter.add_layer("a")
        exporter.add_shape(faces[-1].center_location.inverse() * faces[-1], "a")
        exporter.add_layer("b")
        exporter.add_shape(faces[-1].center_location.inverse() * faces[-2], "b")
    else:
        exporter.add_shape(faces[-1].center_location.inverse() * faces[-1], "{}_a".format(name))

    
    exporter.write("output/{}.dxf".format(name))

for (name, part, multiface) in [
    ("front", front, False),
    ("side", side, True), 
    ("side_b", side_b, True),
    ("roof", roof, False), 
    ("roof_b", roof_b, False),
    ("flr", flr, False),
    ("flr_align", flr_align, False),
    ("back", back, False),
    ("bracket_in", bracket_in, False),
    ("slot", slot, False),
    ("bracket_out", bracket_out, False),
    ("spring", spring, False)
]:
    save_dxfs(name, part, multiface)