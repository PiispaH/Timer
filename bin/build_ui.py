#!/usr/bin/env python3

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils import UI_FOLDER_PATH


def build_ui(i_filepath, o_filepath):
    print("==== building", os.path.basename(o_filepath), "====")
    return_code = os.system(f'pyside6-uic  "{i_filepath}" -o "{o_filepath}"')
    return return_code


def main():
    args = sys.argv[1:]
    if args and not len(args) == 2:
        print("Not valid inputs.")
        return
    elif args:
        return build_ui(args[0], args[1])
    else:
        for path in os.listdir(os.path.join(UI_FOLDER_PATH, "src")):
            file_name, extension = os.path.splitext(path)
            if extension == ".ui":
                code = build_ui(
                    os.path.join(UI_FOLDER_PATH, "src", path),
                    os.path.join(UI_FOLDER_PATH, file_name + ".py"),
                )
                if code:
                    print("something went wrong with", path)
                    return


if __name__ == "__main__":
    main()
