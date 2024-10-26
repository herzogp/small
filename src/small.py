import argparse
import os
import sys
from pathlib import PurePath

# from colors import COLOR_CYAN, print_color, COLOR_YELLOW, COLOR_ENDC, COLOR_RED

COLOR_ON_BLUE = "\033[44m"
COLOR_ON_RED = "\033[41m"
COLOR_ON_DARK_GREY = "\033[100m"
COLOR_ON_BLACK = "\033[40m"

COLOR_RED = "\033[0;31m"
COLOR_GREEN = "\033[0;32m"
COLOR_CYAN = "\033[0;36m"
COLOR_BLACK = "\033[30m"
COLOR_BLUE = "\033[34m"
COLOR_WHITE = "\033[97m"
COLOR_LIGHT_GREY = "\033[37m"
COLOR_LIGHT_BLUE = "\033[94m"

COLOR_ENDC = "\033[0m"

STYLE_STRIKE = "\033[9m"
STYLE_BOLD = "\033[1m"
STYLE_DARK = "\033[2m"

# class LineInfo():
#     def __init__(self, lno: int):
#         self._lno = lno
# 
#     @property
#     def lno(self) -> int:
#         return self._lno
# 
#     @lno.setter
#     def lno(self, lno: int):
#         self._lno = lno
# 
# def configure_line_writer(args):
#     region_color = f"\033[;{args.region_color}m"
#     def line_writer(line: str, info: LineInfo) -> bool:
#         color = ""
#         stripped_line = line.lstrip()
#         if stripped_line.startswith('def '):
#             color = region_color
#         elif stripped_line.startswith('@'):
#             color = STYLE_BOLD + COLOR_ON_BLUE + COLOR_BLACK
#         if color == "":
#             colored_line = line
#         else:
#             colored_line = f"{color}{line}{COLOR_ENDC}"
#         numbered_line = f"{info.lno:4d} {colored_line}"
#         print(numbered_line)
#         return True
#     return line_writer
# 
# def readlines(fname: str, writer) -> list[str]:
#     all_lines = []
#     with open(fname) as f:
#         lno = 0
#         line_info = LineInfo(lno)
#         for line in f:
#             just_line = line.rstrip()
#             lno = lno + 1
#             line_info.lno = lno
#             writer(just_line, line_info)
#             all_lines.append(just_line)
#     return all_lines
# 
# def show_regions(args):
#     lw = configure_line_writer(args)
#     readlines(args.target_file, lw)
# 
# reg_colors = {
#     "black": 30,
#     "grey": 30,
#     "red": 31,
#     "green": 32,
#     "yellow": 33,
#     "blue": 34,
#     "magenta": 35,
#     "cyan": 36,
#     "light_grey": 37,
#     "dark_grey": 90,
#     "light_red": 91,
#     "light_green": 92,
#     "light_yellow": 93,
#     "light_blue": 94,
#     "light_magenta": 95,
#     "light_cyan": 96,
#     "white": 97,
# }

def did_build_target(cwd: str, proj_name: str) -> bool:
    cwd_name = PurePath(cwd).name
    if cwd_name == proj_name:
        target_path = cwd
    else:
        target_path = os.path.join(cwd, proj_name) 

    if not os.path.isdir(target_path):
        os.mkdir(target_path) 
        print(f"Created '{target_path}'") 
  
    # make sure target_path exists and is empty
    if not os.path.isdir(target_path):
        print(f"target directory not accessible: '{target_path}'")
        return False

    nx = len(os.listdir(target_path))
    if nx > 0:
        print(f"target directory is not empty: '{target_path}'")
        return False
    return True


def small():
    cwd = os.getcwd()
    cwd_name = PurePath(cwd).name
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("base_name", nargs='?', help="Base name for project - defaults to current directory name", default=cwd_name)

    args = arg_parser.parse_args()
    # print(f"base_name: {args.base_name}")

    target_prepared = did_build_target(cwd, args.base_name)
    if target_prepared:
        print(f"target '{args.base_name}' is prepared")
    else:
        os._exit(1)
    print("Did not exit")


if __name__ == '__main__':
    small()


