# Make Small

## mksmall cli

    $ python mksmall.py base_name

argparse

args.base_name


## example

    $ python mksmall.py readcat

## underlying actions

    $ mkdir args.base_name
    $ cd args.base_name

## file .gitignore
```
.venv
**/__pycache__
*.egg-info
*.pyd
build
deploy_*
dist
result
```

## file shell.nix
```
let
  pkgs = import <nixpkgs> {};
in pkgs.mkShell {
  packages = [
    pkgs.python3
    (pkgs.python3.withPackages (ps: with ps; [
      black
      build
      mypy
      pdoc
      pip
      pylint
      pytest
      setuptools
      wheel
    ]))
  ];
}
```
## file default.nix
```
let
  pkgs = import <nixpkgs> {};
  sdk_version = (builtins.fromTOML(builtins.readFile( ./pyproject.toml))).project.version;
in
  with pkgs;
  python3.pkgs.buildPythonPackage {
    pname = "antithesis-sdk-python";
    version = sdk_version;
    format = "pyproject";
    src = ./.;
    propagatedBuildInputs = with python3.pkgs; [
      setuptools
      cython
      cffi
    ];
  }
```

## file LICENSE
```
MIT License

Copyright (c) ${this_year} ${args.org}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## file README.md
```
${args.base_name}
================= '=' * len(args.base_name)

Start a development shell to install build tools to the working environment:

    $ nix-shell


Tools installed includes: 

- black
- build
- mypy
- pdoc
- pip
- pylint
- pytest
- python3
- setuptools
- wheel

To format source:

		$ black [--check] src

To evaluate with type hints:

		$ mypy

To perform linting:

    $ pylint src

To perform testing:

    $ pytest

To build distributions:

    $ python -m build

To view docs:

    $ pdoc -d google --no-show-source -p 7070 -n src/*.py
    # browse http://localhost:7070/

To smoke-test:

		$ ./result/bin/${args.base_name}
```

## pyproject.toml
```
[project]
name = "${args.base_name}"
version = "0.1.0"
description = "${args.desc}"
license = {file = "LICENSE"}
readme = "README.md"

[tool.black]
verbose = true

[tool.mypy]
files = "src/*.py"

[tool.pylint.messages_control]
# disable = "C0114,C0115,C0116"

[tool.pytest.ini_options]
pythonpath = ["src", "tests"]

[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project.scripts]
${args.base_name} = "${args.base_name}:${args.base_name}"
```

