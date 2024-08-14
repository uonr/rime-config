#!/usr/bin/env python3

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from optparse import OptionParser
import subprocess

import patch

parser = OptionParser()

parser.add_option("-p", "--path", dest="rime_path",
                  help="The path of rime configurations", metavar="PATH")

class MyHandler(FileSystemEventHandler):
    def __init__(self, filename, callback):
        self.filename = filename
        self.callback = callback

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(self.filename):
            print(f"File {self.filename} has been modified")
            self.callback()


if __name__ == "__main__":
    (options, args) = parser.parse_args()
    if options.rime_path is None:
        print("Please specify the path of rime configurations")
        exit(1)
    filename = "table.txt"
        
    def run_on_change():
        print("File changed! Patching...")
        patch.patch(rime_path=options.rime_path)
    event_handler = MyHandler(filename, run_on_change)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
