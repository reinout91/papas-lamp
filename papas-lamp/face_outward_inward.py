from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Cylinder
from OCP.gp import gp_Pnt, gp_Vec, gp_Dir
from OCP.BRepLProp import BRepLProp_SLProps
from OCP.TopAbs import TopAbs_REVERSED

def is_face_hole_or_pin(topods_face):
    """
    Determines if a cylindrical face corresponds to a hole or a pin by checking
    the direction of the normals.

    :param topods_face: A TopoDS_Face object from Build123d (mybuild123face.wrapped)
    :return: "hole" if normals point inward, "pin" if normals point outward
    """
    # Access the surface using BRepAdaptor_Surface
    surface_adaptor = BRepAdaptor_Surface(topods_face)

    # Check if the surface is a cylinder
    if surface_adaptor.GetType() != GeomAbs_Cylinder:
        raise ValueError("The provided face is not a cylindrical surface.")

    # Get the cylindrical surface's axis and reference point
    cylinder = surface_adaptor.Cylinder()
    location = cylinder.Axis().Location()  # gp_Pnt
    axis_direction = cylinder.Axis().Direction()  # gp_Dir

    # Evaluate mid-point parameters on the surface
    u_mid = (surface_adaptor.FirstUParameter() + surface_adaptor.LastUParameter()) / 2
    v_mid = (surface_adaptor.FirstVParameter() + surface_adaptor.LastVParameter()) / 2

    # Create a property evaluator for the face
    props = BRepLProp_SLProps(surface_adaptor, u_mid, v_mid, 1, 1e-6)
    if not props.IsNormalDefined():
        raise ValueError("Normal could not be defined for the given face.")

    # Get the normal vector at the point
    normal_vector = props.Normal()  # gp_Dir

    # Get a point on the surface
    point_on_surface = props.Value()  # gp_Pnt

    # Vector from the axis location to the point on the surface
    radial_vector = gp_Vec(location, point_on_surface)

    # Normalize the radial vector to create a gp_Dir
    radial_direction = gp_Dir(radial_vector)

    # Dot product to determine direction
    dot_product = normal_vector.Dot(radial_direction)

    # Adjust for face orientation
    if topods_face.Orientation() == TopAbs_REVERSED:
        dot_product = -dot_product

    # Debugging output
    # print("Normal Vector:", normal_vector.Coord())
    # print("Radial Direction:", radial_direction.Coord())
    # print("Dot Product:", dot_product)
    # print("Face Orientation:", topods_face.Orientation())

    if dot_product < 0:
        return "hole"  # Normals point inward
    else:
        return "pin"  # Normals point outward
