import build123d as bd
from ocp_vscode import Camera, show_all

p = bd.Part(None) + bd.Box(length=30, width=60, height=30)

show_all(reset_camera=Camera.KEEP)
