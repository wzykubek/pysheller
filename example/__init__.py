from pysheller import PySheller
from os import path

cmd_dir_path = path.dirname(path.realpath(__file__))

PySheller(
    name="test-app",
    description="Very example app.",
    commands_dir=path.join(cmd_dir_path, "commands"),
)
