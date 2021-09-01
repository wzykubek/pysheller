from os import listdir, path
from argparse import ArgumentParser
from subprocess import call
import re


class PySheller:
    def __init__(self, app_name: str, app_description: str, scripts_dir: str) -> None:
        self.app = app_name
        self.desc = app_description
        self.__directory = path.abspath(scripts_dir)
        self.commands = self.get_commands()
        self.parse_args()
        self.run()

    def get_commands(self) -> list:
        files = listdir(self.__directory)
        cmds = []
        for f in files:
            name, ext = path.splitext(f)
            if ext in [".sh", ".bash", ".zsh"]:
                cmds.append(name)
        return cmds

    def get_path(self, command: str) -> str:
        return path.join(self.__directory, f"{command}.sh")

    def parse_comments(self, command: str) -> dict:
        with open(self.get_path(command), "r") as cf:
            lines = cf.read().splitlines()
            comments = [
                line.replace("#", "")
                for line in lines
                if line.startswith("#") and not line.startswith("#!")
            ]

            parameters = {"help": None, "args": []}
            for key, val in [line.split(" : ") for line in comments]:
                key, val = key.strip(), val.strip()
                if key == "help":
                    parameters["help"] = val
                elif bool(re.match(r"arg\d+$", key)):
                    name, desc = [x.strip() for x in val.split(" - ")]
                    parameters["args"].append({"name": name, "help": desc})

        return parameters

    def parse_args(self) -> None:
        self.arg_parser = ArgumentParser(
            prog=self.app, description=self.desc, allow_abbrev=False
        )
        subparsers = self.arg_parser.add_subparsers(dest="command", required=True)

        subcommands = {}
        for cmd in self.commands:
            p = self.parse_comments(cmd)
            subcommands[cmd] = subparsers.add_parser(cmd, help=p["help"])

            if "args" in p:
                for arg in p["args"]:
                    subcommands[cmd].add_argument(arg["name"], help=arg["help"])
        self.args = self.arg_parser.parse_args()

    def run_command(self, command: str) -> None:
        args = [x[1] for x in self.args._get_kwargs() if x[1] is not None]
        call(self.get_path(args[0]) + " " + " ".join(args[1:]), shell=True)

    def run(self) -> None:
        self.run_command(self.args.command)
