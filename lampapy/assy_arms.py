import copy
from enum import Enum, auto

from assy_leaf import assy_leaf
from build123d import (
    Compound,
)
from ocp_vscode import Camera, set_port, show

arms = [copy.copy(assy_leaf) for i in range(1, 5)]
# AttributeError: 'list' object has no attribute 'values'

assy_arms = Compound(arms)

if __name__ == "__main__":
    set_port(3939)
    show(assy_arms, reset_camera=Camera.KEEP)
