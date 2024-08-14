import os
import sys
import shutil

from sys import platform

def find_rime_path():
    rime_path = None
    if platform == "darwin":
        rime_path = os.path.expanduser("~/Library/Rime")
    elif platform.startswith("linux"):
        rime_path = os.path.expanduser("~/.local/share/fcitx5/rime")
    if rime_path is None or not os.path.exists(rime_path):
        print("Rime configuration path not found.")
        exit(1)
    return rime_path

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


def patch(rime_path):
    top_list = []
    last_list = []
    
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
    with open("table.txt") as file_to_patch:
        for line in file_to_patch.readlines():
            line = line.strip()
            if line.startswith("#") or line == "":
                continue

            if line.endswith("# top"):
                top_list.append(line[:-5])
            else:
                last_list.append(line)
    
    check_dup()
    patch_file(os.path.join(rime_path, "flypy_top.txt"), top_list)
    patch_file(os.path.join(rime_path, "flypy_user.txt"), last_list)
    shutil.copy("flypy.custom.yaml", rime_path)
