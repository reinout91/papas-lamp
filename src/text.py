from build123d import *
from ocp_vscode import show

with BuildPart() as example:
    Box(100, 100, 5)
    with BuildSketch(example.faces().sort_by(Axis.Z)[-1]):
        Text("sample", font_size=20)
    extrude(amount=2)

show(example)