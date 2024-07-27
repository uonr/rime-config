#!/usr/bin/env python3
import subprocess

text = input("Text: ")
code = input("Code: ")

with open("table.txt", "a") as patch_file:
    patch_file.write(f"{text}\t{code}\n")
subprocess.run(["python3", "patch_flypy.py"])
print("Patch added.")
