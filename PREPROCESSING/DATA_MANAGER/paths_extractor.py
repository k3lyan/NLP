# !/usr/bin/python
import os

def path_generator():
    paths = []
    for root, dirs, files in os.walk("./data/CF_passy", topdown=False):
        for name in files:
            paths.append(os.path.join(root, name))
        for name in dirs:
            paths.append(os.path.join(root, name))
    with open('initial_paths', 'w') as paths_file:
        paths_file.write('\n'.join(paths))
        paths_file.close()

path_generator()
