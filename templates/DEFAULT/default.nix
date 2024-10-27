let
  pkgs = import <nixpkgs> {};
  pkg_version = (builtins.fromTOML(builtins.readFile( ./pyproject.toml))).project.version;
in
  with pkgs;
  python3.pkgs.buildPythonPackage {
    pname = "[.BASE_NAME.]";
    version = pkg_version;
    format = "pyproject";
    src = ./.;
    propagatedBuildInputs = with python3.pkgs; [
      setuptools
    ];
  }
