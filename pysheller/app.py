from os import listdir, path
from argparse import ArgumentParser
from subprocess import call
import re
from collections import OrderedDict


class PySheller:
    def __init__(self, name: str, description: str, commands_dir: str) -> None:
        self.app = name
        self.desc = description
        self.__directory = path.abspath(commands_dir)
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

    def get_file_path(self, command: str) -> str:
        return path.join(self.__directory, f"{command}.sh")

    def parse_comments(self, command: str) -> dict:
        with open(self.get_file_path(command), "r") as cf:
            lines = cf.read().splitlines()
            comments = [
                line.replace("#", "")
                for line in lines
                if line.startswith("#") and not line.startswith("#!")
            ]

            parameters = {"help": None, "args": {}}

            for key, val in [line.split(" : ") for line in comments]:
                key, val = key.strip(), val.strip()
                if key == "help":
                    parameters["help"] = val
                elif bool(re.match(r"arg\d+$", key)):
                    name, desc = [x.strip() for x in val.split(" - ")]
                    id_ = int(key.split("arg")[1])
                    parameters["args"][id_] = {"name": name, "help": desc}

            parameters["args"] = dict(OrderedDict(sorted(parameters["args"].items())))

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
                for arg in p["args"].items():
                    subcommands[cmd].add_argument(arg[1]["name"], help=arg[1]["help"])
        self.args = self.arg_parser.parse_args()

    def run_command(self, command: str) -> None:
        args = []
        for exp_args in self.parse_comments(command)["args"].items():
            id_, arg = exp_args
            passed_arg = self.args.__getattribute__(re.sub(r"^--", "", arg["name"]))
            if passed_arg is None:
                args.append("")
            else:
                args.append(passed_arg)
        call(self.get_file_path(command) + " " + " ".join(args), shell=True)

    def run(self) -> None:
        self.run_command(self.args.command)
