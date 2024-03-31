#!/usr/bin/env python3
import os
import sys
import shutil

from sys import platform

top_list = []
last_list = []

# Get the Rime configuration path
rime_path = "."
if platform == "darwin":
    rime_path = os.path.expanduser("~/Library/Rime")
elif platform.startswith("linux"):
    rime_path = os.path.expanduser("~/.local/share/fcitx5/rime")
if not os.path.exists(rime_path):
    print("Rime configuration path not found.")
    exit(1)


with open("table.txt") as patch_file:
    for line in patch_file.readlines():
        line = line.strip()
        if line.startswith("#") or line == "":
            continue

        if line.endswith("# top"):
            top_list.append(line[:-5])
        else:
            last_list.append(line)

def check_dup():
    record = set()
    for item in top_list:
        word = item.split("\t")[0]
        if word in record:
            print(f"Duplicate word: {word}")
        record.add(line)
    for item in last_list:
        word = item.split("\t")[0]
        if word in record:
            print(f"Duplicate word: {word}")
        record.add(line)
check_dup()



PATCH_START_MARK = "### PATCH START ###"
PATCH_END_MARK = "### PATCH END ###"

def patch_file(file_path, patch_lines):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    overwrite_lines = []
    in_patch = False
    with open(file_path) as file:
        for line in file.readlines():
            line = line.strip()
            if line == PATCH_START_MARK:
                in_patch = True
                continue
            if line == PATCH_END_MARK:
                in_patch = False
                continue
            if in_patch:
                continue
            overwrite_lines.append(line)
        overwrite_lines.append(PATCH_START_MARK)
        overwrite_lines.extend(patch_lines)
        overwrite_lines.append(PATCH_END_MARK)

    with open(file_path, "w") as overwrite_file:
        overwrite_file.write("\n".join(overwrite_lines))

patch_file(os.path.join(rime_path, "flypy_top.txt"), top_list)
patch_file(os.path.join(rime_path, "flypy_user.txt"), last_list)
shutil.copy("flypy.custom.yaml", rime_path)