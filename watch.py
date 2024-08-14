#!/usr/bin/env python3

import time
from optparse import OptionParser
import os
import patch

parser = OptionParser()

parser.add_option("-p", "--path", dest="rime_path",
                  help="The path of rime configurations", metavar="PATH")


if __name__ == "__main__":
    (options, args) = parser.parse_args()
    rime_path = options.rime_path
    if rime_path is None:
        rime_path = patch.find_rime_path()
    filename = "table.txt"
        
    def run_on_change():
        print("File changed! Patching...")
        patch.patch(rime_path=rime_path)

    mtime = os.path.getmtime(filename)
    size = os.path.getsize(filename)
    while True:
        # Check if the file changes
        current_mtime = os.path.getmtime(filename)
        current_size = os.path.getsize(filename)
        if mtime != current_mtime or size != current_size:
            mtime = current_mtime
            size = current_size
            run_on_change()
        time.sleep(2)
