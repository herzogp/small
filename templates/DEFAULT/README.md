[.BASE_NAME.]
[. $replace('=', BASE_NAME) .]

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

		$ ./result/bin/addx 27 410

		$ ./result/bin/[.BASE_NAME.]

