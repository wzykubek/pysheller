# pysheller

Simple, small and **experimental** Python library to create Python CLI application using shell scripts and magic comments to add commands and arguments and generate help message automatically. Initially created for [guzzy](https://github.com/samedamci/guzzy) but can be used for any other project.

## Installing

```shell
$ python -m pip install pysheller
```

## Usage Example

Sample directory structure:

```
app
├── cmd
│   ├── command1.sh
│   ├── command2.sh
│   └── command3.sh
└── __init__.py

```

Main Python file:

```python
from pysheller import PySheller
from os import path

cmd_dir = path.dirname(path.realpath(__file__))

PySheller(
  name="example",
  description="Description of the app.",
  commands_dir="./cmd"
)
```

Command script:

```bash
#!/bin/sh

# help : help message for the command
# arg1 : argument : help message for argument 1
# arg2 : --foo : help message for argument 2

echo "$1" "$2"
```
