from enum import Enum, auto

from build123d import (
    Axis,
    BuildPart,
    Face,
    GeomType,
    Part,
    RevoluteJoint,
    RigidJoint,
    add,
)
from ocp_vscode import Camera, set_port, show_all

from .hinge_lever import shackle, t_hinge


# for visualistation purpose
class CylinderType(Enum):
    PIN = auto()
    HOLE = auto()


def get_cylindric_faces_and_axes(
    part: Part, cylinder_type: CylinderType | None = None
) -> list[tuple[Face, Axis]]:
    def get_axis_from_face(face: Face) -> Axis:
        position = 0.5 * (face.position_at(0, 0.5) + face.position_at(0.5, 0.5))
        direction = next(
            edge.location_at(1).to_axis().direction
            for edge in face.edges()
            if not edge.is_closed
        )
        return Axis(position, direction)

    def is_valid_candidate(face: Face) -> bool:
        center_position = 0.5 * (face.position_at(0, 0.5) + face.position_at(0.5, 0.5))
        is_inside = part.is_inside(center_position)

        if cylinder_type == CylinderType.HOLE:
            return not is_inside
        if cylinder_type == CylinderType.PIN:
            return is_inside
        return True

    faces = part.faces().filter_by(GeomType.CYLINDER)
    valid_faces = (
        face for face in faces if any(edge.is_closed for edge in face.edges())
    )

    filtered_faces = filter(is_valid_candidate, valid_faces)

    return [(face, get_axis_from_face(face)) for face in filtered_faces]


with BuildPart():
    add(shackle)
    add(t_hinge)
    shackle.color = "red"

    axis_of_hinge = -get_cylindric_faces_and_axes(t_hinge.part, CylinderType.HOLE)[0][1]
    axis_of_shackle = get_cylindric_faces_and_axes(shackle.part, CylinderType.PIN)[2][
        1
    ].location

    j1 = RevoluteJoint(label="t_hinge_hole", to_part=t_hinge.part, axis=axis_of_hinge)
    j2 = RigidJoint(
        label="shackle_pin", to_part=shackle.part, joint_location=axis_of_shackle
    )

    j1.connect_to(j2, angle=20)


set_port(3939)
show_all(reset_camera=Camera.KEEP)
