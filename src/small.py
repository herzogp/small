import argparse
import os
import sys
from pathlib import PurePath

TEMPLATE_BASE_DIR = "/home/pherzog/Projects/Python/small/templates"
DEFAULT_TEMPLATE_NAME = "DEFAULT"

RESERVED_WORDS = [
    'and', 'as', 'assert', 
    'break', 'class', 'continue',
    'def', 'del',
    'elif', 'else', 'except',
    'False', 'finally', 'for', 'from',
    'global',
    'if', 'import', 'in', 'is',
    'lambda',
    'None', 'nonlocal', 'not',
    'or',
    'pass',
    'raise', 'return',
    'True', 'try',
    'while', 'with',
    'yield'
]

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

def get_target_path(cwd: str, proj_name: str) -> str:
    cwd_name = PurePath(cwd).name
    if cwd_name == proj_name:
        target_path = cwd
    else:
        target_path = os.path.join(cwd, proj_name) 

    if not os.path.isdir(target_path):
        os.mkdir(target_path) 
        print(f"Created '{target_path}'") 
    return target_path

def did_build_target(target_path: str) -> bool:
    """make sure target_path exists and is empty"""
    if not os.path.isdir(target_path):
        # print(f"target directory not accessible: '{target_path}'")
        return False

    nx = len(os.listdir(target_path))
    if nx > 0:
        # print(f"target directory is not empty: '{target_path}'")
        return False
    return True

def template_path(template_name: str) -> str:
    template = DEFAULT_TEMPLATE_NAME if template_name == "" else template_name
    template_path = os.path.join(TEMPLATE_BASE_DIR, template)
    return template_path

def reify_template(template_path: str, target_path: str) -> bool:
    pass

def clean_base_name(name: str) -> str:
    # replace whitespace and non-ascii chars with '_'
    # if leading character is not A-Z,a-z,_ prepend('_')
    # if name is a reserved word, prepend '_'
    base_name = name.strip()
    if base_name in RESERVED_WORDS:
        base_name = '_' + base_name

    if base_name.isidentifier():
        return base_name

    result = []
    first = True
    for c in base_name:
        new_c = '_'
        if c.isalnum() or c == '_':
            new_c = c
        if first:
            first = False
            if not c.isalpha():
                result.append('_')
        result.append(new_c)
    return ''.join(result)

def handle_file(file_path: str):
    print(f"   {file_path}")

def handle_dir(dir_path: str):
    print(f"{dir_path}")

def did_process_template(template_name: str, from_path: str) -> bool:
    nfiles = 0
    ndirs = 1
    result = True
    for root, dirs, files in os.walk(from_path):
        for filename in files:
            nfiles = nfiles + 1
            handle_file(os.path.join(root, filename))
        for dirname in dirs:
            ndirs = ndirs + 1
            handle_dir(os.path.join(root, dirname))

    if nfiles == 0:
        print()
        print(f"No files found for template '{template_name}'")
        result = False
    else:
        files_msg = "files" if nfiles != 1 else "file"
        dirs_msg = "directories" if ndirs != 1 else "directory"
        print()
        print(f"Template '{template_name}' provided {nfiles} {files_msg} in {ndirs} {dirs_msg}")
    return result

def small():
    cwd = os.getcwd()
    cwd_name = PurePath(cwd).name
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("base_name", nargs='?', help="Base name for project - defaults to current directory name", default=cwd_name)
    arg_parser.add_argument("--template_name", "-t", help="Template name", default="")
    args = arg_parser.parse_args()
    base_name = clean_base_name(args.base_name)
    template_name = args.template_name.strip()

    target_path = get_target_path(cwd, base_name)
    target_prepared = did_build_target(target_path)

    if not target_prepared:
        print(f"'{target_path}' is not empty or is inaccessible")
        os._exit(1)

    from_path = template_path(template_name)
    if template_name == "":
        template_name = DEFAULT_TEMPLATE_NAME
    if did_process_template(template_name, from_path):
        print(f"Done")
    else:
        os._exit(2)

if __name__ == '__main__':
    small()


