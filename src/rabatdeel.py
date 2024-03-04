from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
set_port(3939)

import build123d as b3d
import cadquery as cq
import duckdb as ddb
import pyarrow as pa

from enum import Enum


Axis = b3d.Axis
Compound = b3d.Compound
Locations = b3d.Locations
BuildPart = b3d.BuildPart
Box = b3d.Box
GridLocations = b3d.GridLocations
Cylinder = b3d.Cylinder
Sphere = b3d.Sphere
Location = b3d.Location
HexLocations = b3d.HexLocations
b3dcopy=b3d.copy

bottom_height = 7
top_height = 3
left_window_width = 1000
right_window_width = 1200
n_lower_part = 5
n_top_part = 3

rabat_regelafstand = 143

c_name="name"
c_length = "length"
c_count = "count"
t_dimensions = "dimensions"

dimensions = pa.Table.from_pydict({c_name: ['rabat_top', 'rabat_left', 'rabat_mid', 'rabat_right'],
        c_length: [5100, 1200, 1400, 1400],
        c_count:[n_top_part, n_lower_part, n_lower_part, n_lower_part]})


def rabatDeel(length):
    profile = cq.importers.importDXF("src/imported/rabatdeel.dxf").wires().toPending().extrude(1).findSolid()
    b3d_solid = b3d.Solid.make_box(1,1,1)
    #The way to exchange from cq to b3d: https://build123d.readthedocs.io/en/latest/tips.html
    b3d_solid.wrapped = profile.wrapped
    b3d_solid = b3d_solid.rotate(Axis.Y,180)
    b3d_solid = b3d_solid.rotate(Axis.Y,90)
    scaled_rabat = b3d.scale(b3d_solid, by=(length, 1, 1))

    return(scaled_rabat)

def startProfile(length):
    profile = cq.importers.importDXF("src/imported/startprofile.dxf").wires().toPending().extrude(1).findSolid()
    b3d_solid = b3d.Solid.make_box(1,1,1)
    #The way to exchange from cq to b3d: https://build123d.readthedocs.io/en/latest/tips.html
    b3d_solid.wrapped = profile.wrapped
    b3d_solid = b3d_solid.rotate(Axis.Y,90)
    scaled_startprofile = b3d.scale(b3d_solid, by=(length, 1, 1))

    return(scaled_startprofile)

def ventilation(length):
    profile = cq.importers.importDXF("src/imported/ventilation_30.dxf").wires().toPending().extrude(1).findSolid()
    b3d_solid = b3d.Solid.make_box(1,1,1)
    #The way to exchange from cq to b3d: https://build123d.readthedocs.io/en/latest/tips.html
    b3d_solid.wrapped = profile.wrapped
    b3d_solid = b3d_solid.rotate(Axis.Y,90)
    scaled_startprofile = b3d.scale(b3d_solid, by=(length, 1, 1))

    return(scaled_startprofile)


def lekdorpel(length):
    profile = cq.importers.importDXF("src/imported/lekdorpel.dxf").wires().toPending().extrude(1).findSolid()
    b3d_solid = b3d.Solid.make_box(1,1,1)
    #The way to exchange from cq to b3d: https://build123d.readthedocs.io/en/latest/tips.html
    b3d_solid.wrapped = profile.wrapped
    b3d_solid = b3d_solid.rotate(Axis.Y,90)
    scaled_startprofile = b3d.scale(b3d_solid, by=(length, 1, 1))

    return(scaled_startprofile)


def rabatPanel(panel):
    v_rabat = f"'{panel}'"
    rabat_length =  ddb.sql(f"SELECT {c_length} FROM {t_dimensions} WHERE {c_name} = {v_rabat}").fetchone()[0]
    rabat_right = rabatDeel(rabat_length)

    locs = GridLocations(x_spacing = 0,
                        y_spacing = rabat_regelafstand,
                        x_count = 1,
                        y_count = 5
                        ).local_locations

    rabatdeelPanel = [b3dcopy.copy(rabat_right).locate(loc) for loc in locs]
    for i in rabatdeelPanel:
        i.label="rabatdeel"

    reference_assembly = Compound(children=rabatdeelPanel)

    reference_assembly.label = panel
    return(reference_assembly)

rabat_mid = rabatPanel('rabat_mid')
rabat_mid.position += (-1700,0,0)

rabat_left = rabatPanel('rabat_left')
rabat_left.position += (-(5100-1200),0,0)

rabat_top = rabatPanel('rabat_top')
rabat_top.position += (0,5*143,0)

rabat_panelset = Compound(
    children=[
        rabatPanel('rabat_right'),
        rabat_mid,
        rabat_left,
        rabat_top

        ]
    )
rabat_panelset.position += (5100,292.244)

startprofile_left = startProfile(1200).translate((0,23.6,-18.00))
startprofile_left.label = f"startprofile_left"
startprofile_mid = startProfile(1400).translate((2000,23.6,-18.00))
startprofile_mid.label = f"startprofile_mid"

startprofile_right = startProfile(1400).translate((3700,23.6,-18.00))
startprofile_right.label = f"startprofile_right"

ventilation_left = ventilation(1200).translate((0,30.4,-18))
ventilation_left.label = f"ventilation_left"
ventilation_mid = ventilation(1400).translate((0,30.4,-18)).translate((2000,0,0))
ventilation_mid.label = f"ventilation_mid"

ventilation_right = ventilation(1400).translate((0,30.4,-18)).translate((3700,0,0))
ventilation_right.label = f"ventilation_right"

lekdorpel_left = lekdorpel(800).translate((1200,702,-14.79-15))
lekdorpel_right = lekdorpel(300).translate((3400,702,-14.79-15))

startprofile_left_window = startProfile(800).translate((1200,738,-14.79-3.4))
ventilation_left_window = ventilation(800).translate((1200,738+6.8,-14.79-3.4))
ventilation_left_window.label = f"ventilation_left_window"


rabatdelen_met_strips = Compound(
    children=[rabat_panelset,
              startprofile_left,
              startprofile_mid,
              startprofile_right,
              ventilation_left,
              ventilation_mid,
              ventilation_right,
              lekdorpel_left,
              lekdorpel_right,
              startprofile_left_window,
              ventilation_left_window]
)

rabat_panelset.label = f"rabat_panelset"

show(rabatdelen_met_strips)
#c_length} FROM {t_dimensions} WHERE {c_name} = {v_rabat_left}

#regelwerk moet je verjongen (inkeping maken) waar het startprofiel en ventilatie ding komt.
#Daardoor ligt alles mooi vlak.
#lekdorpel boven ramen
#naast ramen een eindprofiel


#20 bij 30 is ventilatieprofiel

#1mm per strekkende meter werking!
#5mm afwateringgaten maken!
#
#Met een breekmes snijdt je het startprofiel op maat.
#-229.244
#kit bovenaan lekdorpels:
#https://www.hornbach.nl/p/soudal-fix-all-high-tack-zwart-kitkoker-290-ml/7107038/?sourceArt=10534108&trackArticleCrossType=vb&url=7107038