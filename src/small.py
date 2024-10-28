import argparse
import datetime
import os
import sys
from pathlib import Path

# TODO: Should be part of the binary dist for 'small'
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

# TODO: Use colors for output
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
# region_color = f"\033[;{reg_colors["magenta"]}m"

class TextReplacer():
    def __init__(self, base_name: str, base_desc: str, owner: str):
        today = datetime.date.today()
        self._year = str(today.year)
        self._owner = owner
        self._base_desc = base_desc
        self._base_name = base_name

    @property
    def base_name(self) -> str:
        return self._base_name

    @property
    def base_desc(self) -> str:
        return self._base_desc

    @property
    def year(self) -> str:
        return self._year

    @property
    def owner(self) -> str:
        return self._owner

    def resolve_text(self, expr) -> str:
        if expr == 'BASE_NAME':
            return self.base_name
        elif expr == 'BASE_DESC':
            return self.base_desc
        elif expr == 'YEAR':
            return self.year
        elif expr == 'OWNER':
            return self.owner
        else:
            return None
    
    def resolve_expr(self, expr: str)-> str:
        resolved_text = self.resolve_text(expr)
        if resolved_text != None:
            return resolved_text

        # $replace('=', BASE_NAME)
        if expr.startswith("$replace"):
            paren_expr = expr[8:].strip()
            lx = len(paren_expr)
            if paren_expr.startswith("(") and paren_expr.endswith(")"):
                arg_expr = paren_expr[1:lx-1]
                all_args = arg_expr.split(',')
                if len(all_args) == 2:
                    arg_0 = all_args[0].strip()
                    arg_1 = all_args[1].strip()
                    arg_value = self.resolve_text(arg_1)
                    len_val = len(arg_1) if arg_value is None else len(arg_value)
                    result = arg_0[1] * len_val
                    return result
        return ""
    
    def rep_string(self, s: str) -> str:
        idx_start = s.find("[.")
        if idx_start == -1:
            return s
        idx_end = s.find(".]", idx_start + 2)
        if idx_end == -1:
            return s
        print(f"s='{s}'  {idx_start = }  {idx_end = }")
        src_expr = s[idx_start + 2 : idx_end].strip()
        text = self.resolve_expr(src_expr)
        before_text = s[0:idx_start]
        after_text = s[idx_end+2:]
        return before_text + text + after_text
   
    def replace_string(self, s: str) -> str:
        done = False
        while not done:
            new_s = self.rep_string(s)
            if new_s == s:
                done = True
            s = new_s
        return s

def get_target_path(cwd: str, proj_name: str) -> str:
    cwd_name = Path(cwd).name
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

def readlines(replacer: TextReplacer, fname: str, outname: str, verbose=False) -> list[str]:
    all_lines = []
    with open(fname) as f:
        with open(outname, "w") as f_out:
            for line in f:
                use_line = replacer.replace_string(line)
                if verbose:
                    print(use_line, end="")
                print(use_line, end="", file=f_out)
                all_lines.append(use_line)
    return all_lines

def handle_file(replacer: TextReplacer, file_path: str, dest_path: str):
    lx = len(file_path)
    lx2 = len(dest_path) + 4
    ndashes = lx if lx > lx2 else lx2
    dashes = '-' * (2 + ndashes)
    print(dashes)
    print(f"{file_path}")
    print(f"==> {dest_path}")
    print(dashes)
    lines = readlines(replacer, file_path, dest_path, True)
    print()

def handle_dir(dir_path: str):
    os.mkdir(dir_path) 


def did_process_template(replacer: TextReplacer, template_name: str, from_path: str, to_path: str) -> bool:
    nfiles = 0
    ndirs = 1
    result = True
    for root, dirs, files in os.walk(from_path):
        rel_ref2 = os.path.relpath(root, from_path) # src, .
        for filename in files:
            nfiles = nfiles + 1
            final_filename = replacer.replace_string(filename)

            dest_path = os.path.join(to_path,rel_ref2)

            file_to_read = os.path.join(root, filename)
            file_to_write = os.path.join(dest_path, final_filename)
            handle_file(replacer, file_to_read, file_to_write)
        for dirname in dirs:
            ndirs = ndirs + 1
            dest_dir = os.path.join(to_path, rel_ref2)
            dir_to_create = Path(os.path.join(dest_dir, dirname)).resolve()
            handle_dir(dir_to_create)

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
    cwd_name = Path(cwd).name
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("base_name", nargs='?', help="Base name for project - defaults to current directory name", default=cwd_name)
    arg_parser.add_argument("--template_name", "-t", help="Template name", default="")
    arg_parser.add_argument("--owner", "-o", help="Source code owner", default="author")
    arg_parser.add_argument("--description", "-d", help="Project description", default="Project description")
    args = arg_parser.parse_args()
    this_base_name = clean_base_name(args.base_name)
    this_desc = args.description
    this_owner = args.owner
    template_name = args.template_name.strip()

    target_path = get_target_path(cwd, this_base_name)
    target_prepared = did_build_target(target_path)

    if not target_prepared:
        print(f"'{target_path}' is not empty or is inaccessible")
        os._exit(1)

    from_path = template_path(template_name)
    if template_name == "":
        template_name = DEFAULT_TEMPLATE_NAME
    replacer = TextReplacer(this_base_name, this_desc, this_owner)
    if not did_process_template(replacer, template_name, from_path, target_path):
        os._exit(2)

if __name__ == '__main__':
    small()
