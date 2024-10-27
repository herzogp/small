import argparse
import os
from pathlib import PurePath

def [.BASE_NAME.]():
    cwd = os.getcwd()
    cwd_name = PurePath(cwd).name
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("file_name", nargs='?', help="File name for [.BASE_NAME.]", default=cwd_name)

    args = arg_parser.parse_args()

    print(f"[.BASE_NAME.] {args.file_name}")


if __name__ == '__main__':
    [.BASE_NAME.]()
