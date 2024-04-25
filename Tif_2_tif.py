#!/usr/bin/env python


import os
import sys
import tifffile


TIF_PATTERN = ".tif"


def find_tif_path(source):
    tif_paths = []

    for root, dirs, files, in os.walk(source):
        for file in files:
            if TIF_PATTERN in file.lower():
                path = os.path.join(source, file)
                tif_paths.append(path)

        break

    return tif_paths


def converter(paths_file, paths_target):
    file_name = []

    for i in paths_file:
        file_name = os.path.basename(i)
        new_name = os.path.join(paths_target, file_name)

        tif = tifffile.imread(i)
        tifffile.imwrite(new_name, tif)


def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def main(source, target):
    cwd = os.getcwd()
    source_path = os.path.join(cwd, source)
    target_path = os.path.join(cwd, target)

    tif_paths = find_tif_path(source_path)
    create_dir(target_path)
    converter(tif_paths, target_path)


if __name__ == "__main__":
    args = sys.argv
    if len(args)!=3:
        raise Exception("You must pass a source and target only.")

    source, target = args[1:]
    main(source, target)
