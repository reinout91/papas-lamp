# %%
from ocp_vscode import (
    show,
    show_object,
    reset_show,
    set_port,
    set_defaults,
    get_defaults,
    Camera,
)

set_port(3939)
set_defaults(reset_camera=Camera.KEEP)

import build123d as bd


keycap_opener_orig = bd.import_stl("KeyCap_Opener.stl")
keycap_opener_right = keycap_opener_orig.moved(bd.Location((20, 0, 2)))
keycap_opener_back = keycap_opener_orig.moved(bd.Location((0, 20, 2)))


mkswestl = bd.import_stl("mkswe.stl")


# %%
def sketch_from_wires(wires):
    with bd.BuildSketch() as skt:
        for w in wires:
            with bd.BuildLine():
                bd.add(w)
            bd.make_face()

    return skt.sketch


def mkswe_sthlm_logo():
    mks = bd.import_svg("mkswe_sthlm.svg")
    keys = mks[0:7] + mks[25:]
    archTower = mks[23:25]
    towerDetails = mks[7:23]

    ls14bb = ls[14].sketch.bounding_box()
    with bd.BuildSketch() as cutter:
        with bd.Locations(bd.Location(ls14bb.center())):
            bd.Rectangle(ls14bb.size.X, ls14bb.size.Y)
        bd.add(ls[14].sketch, mode=bd.Mode.SUBTRACT)
    with bd.BuildSketch() as expected_face:
        with bd.Locations(bd.Location(ls14bb.center())):
            bd.Rectangle(ls14bb.size.X, ls14bb.size.Y)
        bd.add(cutter.sketch, mode=bd.Mode.SUBTRACT)

    towerDetails[14] = expected_face.sketch.wire()
    towerDetails.append(mks[21])

    with bd.BuildPart() as base:
        with bd.BuildSketch() as cut_tower:
            bd.add(sketch_from_wires(archTower))
            bd.add(sketch_from_wires(towerDetails), mode=bd.Mode.SUBTRACT)
        bd.extrude(amount=20)

    keys_p = []
    for k in keys:
        with bd.BuildPart() as ppp:
            with bd.BuildSketch():
                with bd.BuildLine():
                    bd.add(k)
                bd.make_face()
            bd.extrude(amount=10, dir=bd.Axis.Z.direction, taper=30)
        if ppp.part.bounding_box().center().Z < 0:
            np = ppp.part.mirror(bd.Plane.XY)
            keys_p.append(np)
        else:
            keys_p.append(ppp.part)

    with bd.BuildPart() as extruded_keys:
        for k in keys_p:
            bd.add(k)

    with bd.BuildPart() as logo:
        bd.add(base.part)
        bd.add(extruded_keys.part.move(bd.Location((0, 0, 20))))
    logo.label = "mkswe_sthlm_logo"
    return logo


l = mkswe_sthlm_logo()
# %%
print(l.part.bounding_box())
scaled = l.part.scale(0.1)
print(scaled.bounding_box())
show(l, scaled)


# %%
def opener():
    with bd.BuildPart() as prt:
        with bd.BuildSketch():
            bd.Rectangle(18, 18)
        bd.extrude(amount=15)

        bd.fillet(prt.edges().filter_by(bd.Axis.Z), 2)
        bd.fillet(prt.faces().sort_by(bd.Axis.Z)[0].edges(), 2)

        with bd.BuildSketch(prt.faces().sort_by(bd.Axis.Z)[-1]):
            bd.Rectangle(14.5, 18)
        bd.extrude(amount=5)

        top = prt.faces().sort_by(bd.Axis.Z)[-1]
        left = prt.faces().sort_by(bd.Axis.X)[0]
        front = prt.faces().sort_by(bd.Axis.Y)[0]

        bd.chamfer(top.edges(), 1.7)

        with bd.BuildSketch(top):
            bd.Rectangle(15, 7.2)
            bd.Rectangle(10.5, 13.6)
        bd.extrude(amount=-16, mode=bd.Mode.SUBTRACT)

        with bd.BuildSketch(top):
            with bd.GridLocations(13, 15.3, 2, 2):
                bd.Rectangle(8, 4)
        bd.extrude(amount=-6, mode=bd.Mode.SUBTRACT)

        with bd.BuildSketch(left):
            with bd.Locations(bd.Location((0, -9.55, 0))):
                with bd.GridLocations(13.2, 1, 2, 1):
                    bd.Circle(1 / 1.5)
        bd.extrude(amount=-20, mode=bd.Mode.SUBTRACT)

        bd.Hole(2.5)

        bd.fillet(
            prt.edges().filter_by_position(bd.Axis.Z, 10, 20)
            # .filter_by(bd.Axis.Z, reverse=True),
            ,
            0.21,
        )

        bd.fillet(
            prt.edges()
            .filter_by_position(bd.Axis.Z, -10, 13)
            .filter_by(bd.Axis.Z, reverse=True),
            0.5,
        )
        with bd.BuildSketch(front):
            bd.Text(
                "Stockholm",
                font_size=2.3,
                font_style=bd.FontStyle.BOLD,
                align=(bd.Align.CENTER, bd.Align.MIN),
            )
            with bd.Locations(bd.Location((0, -0.3, 0))):
                bd.Text(
                    "Meetup 8",
                    font_size=2.3,
                    font_style=bd.FontStyle.BOLD,
                    align=(bd.Align.CENTER, bd.Align.MAX),
                )
            with bd.Locations(bd.Location((0, -5, 0))):
                bd.Text(
                    "2024-02-24",
                    font_size=2,
                    font_style=bd.FontStyle.BOLD,
                    align=(bd.Align.CENTER, bd.Align.MAX),
                )
        bd.extrude(amount=0.3)

    return prt.part


# svg = __file__.replace("switch-opener.py", "atom.svg")
# print(svg)
# t = bd.import_svg(svg)
part = opener()  # .move(bd.Location((0, 0, -2)))
show(part)
# %%
logo = mkswe_sthlm_logo()
# %%
slogo = logo.part.scale(0.018)
# %%

rslogo = (
    slogo.rotate(bd.Axis.X, 90).rotate(bd.Axis.Z, 180).move(bd.Location((5.4, 8.9, 2)))
)
show(
    part,
    rslogo,
)

# %%
with bd.BuildPart() as mkswe_opener:
    bd.add(part)
    bd.add(rslogo)

show(mkswe_opener)
mkswe_opener.part.export_step(__file__.replace(".py", "_mkswe_sthlm_8.step"))
mkswe_opener.part.export_stl(__file__.replace(".py", "_mkswe_sthlm_8.stl"))
# %%
atom = bd.import_svg("atom.svg")
print(type(atom))
print(atom)
with bd.BuildPart() as msp:
    with bd.BuildSketch():
        bd.add(atom.wires())
        bd.add(atom.faces())
    bd.extrude(amount=1)
show(msp, atom.wires(), atom.faces())
# %%
mks = bd.import_svg("mkswe_sthlm.svg")
print(mks)
print(len(mks))
# 23+24 is the big piece, cut all other shapes out of that?
# %%
ls = []
for i, w in enumerate(mks):
    with bd.BuildSketch() as skt:
        with bd.BuildLine():
            bd.add(w)
        bd.make_face()
    skt.label = str(i)
    ls.append(skt)
show(ls)
# %%
print(ls[14].sketch.bounding_box())
print(ls[14].sketch.location)
print(ls[14].sketch.faces()[0].location)

ls14bb = ls[14].sketch.bounding_box()
with bd.BuildSketch() as cutter:
    with bd.Locations(bd.Location(ls14bb.center())):
        bd.Rectangle(ls14bb.size.X, ls14bb.size.Y)
    bd.add(ls[14].sketch, mode=bd.Mode.SUBTRACT)
with bd.BuildSketch() as expected_face:
    with bd.Locations(bd.Location(ls14bb.center())):
        bd.Rectangle(ls14bb.size.X, ls14bb.size.Y)
    bd.add(cutter.sketch, mode=bd.Mode.SUBTRACT)
show(cutter, ls[14], expected_face)
print(expected_face)
print(expected_face.sketch)
print(expected_face.sketch.wire())

# %%
keys = mks[0:7] + mks[25:]
archTower = mks[23:25]
towerDetails = mks[7:23]
towerDetails[14] = expected_face.sketch.wire()
towerDetails.append(mks[21])


def sketch_from_wires(wires):
    with bd.BuildSketch() as skt:
        for w in wires:
            with bd.BuildLine():
                bd.add(w)
            bd.make_face()

    return skt.sketch


keys_skt = sketch_from_wires(keys)
archTower_skt = sketch_from_wires(archTower)
towerDetails_skt = sketch_from_wires(towerDetails)

with bd.BuildSketch() as sss:
    bd.add(archTower_skt)
    bd.add(towerDetails_skt, mode=bd.Mode.SUBTRACT)

show(
    mks,
    keys,
    archTower,
    towerDetails,
    keys_skt,
    archTower_skt,
    towerDetails_skt,
    sss,
)

# %%
keys_p = []
for k in keys:
    with bd.BuildPart() as ppp:
        with bd.BuildSketch():
            with bd.BuildLine():
                bd.add(k)
            bd.make_face()
        bd.extrude(amount=10, dir=bd.Axis.Z.direction, taper=30)
    if ppp.part.bounding_box().center().Z < 0:
        np = ppp.part.mirror(bd.Plane.XY)
        keys_p.append(np)
    else:
        keys_p.append(ppp.part)

show(
    keys_p,
)
# %%
with bd.BuildPart() as base:
    with bd.BuildSketch():
        bd.add(sss)
    bd.extrude(amount=10)

with bd.BuildPart() as button:
    for k in keys_p:
        bd.add(k)

with bd.BuildPart() as logo:
    bd.add(base.part)
    bd.add(button.part.move(bd.Location((0, 0, 10))))
show(
    # keys_p,
    # sss,
    base,
    button.part.move(bd.Location((0, 0, 10))),
    logo,
)
logo.part.export_step(__file__.replace(".py", "_mkswelogo.step"))
logo.part.export_stl(__file__.replace(".py", "_mkswelogo.stl"))
# %%
p = mks[0:23]
q = mks[25:40]
smaller = p + q
with bd.BuildSketch() as details:
    for w in smaller:
        with bd.BuildLine():
            bd.add(w)
        bd.make_face()
with bd.BuildSketch() as bigger:
    for w in mks[23:25]:
        with bd.BuildLine():
            bd.add(w)
        bd.make_face()

with bd.BuildPart() as pp:
    bd.add(bigger.sketch)
    bd.extrude(amount=10)
    bd.add(details.sketch)
    bd.extrude(amount=12)

show(details, bigger, pp)

# pp.part.export_step(__file__.replace(".py", "_mkswelogo.step"))
# pp.part.export_stl(__file__.replace(".py", "_mkswelogo.stl"))
# %%
sub = mks[0:24]

with bd.BuildPart() as mksp:
    with bd.BuildSketch() as mkss:
        for i, w in enumerate(sub):
            with bd.BuildLine():
                bd.add(w)
            bd.make_face()
    bd.extrude(amount=30)

# with bd.BuildPart() as mksp:
#     for w in sub:
#         try:
#             print(w)
#             with bd.BuildLine():
#                 bd.add(w)
#             with bd.BuildSketch():
#                 bd.Rectangle(9,9)
#             bd.sweep()
#         except:
#             print("Did badly")
show(mks, mkss, mksp)
# %%
with bd.BuildPart() as ppp:
    bd.Box(10, 20, 30)
    with bd.BuildSketch(ppp.faces().sort_by(bd.Axis.X)[0]):
        bd.Text(
            "Meetup9", font_size=8, align=(bd.Align.CENTER, bd.Align.MIN), rotation=-90
        )
        bd.Text(
            "2024-02-24",
            font_size=8,
            align=(bd.Align.CENTER, bd.Align.MAX),
            rotation=-90,
        )
    bd.extrude(amount=2)

show(ppp)