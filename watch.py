#!/usr/bin/env python3

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

class MyHandler(FileSystemEventHandler):
    def __init__(self, filename, callback):
        self.filename = filename
        self.callback = callback

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(self.filename):
            print(f"File {self.filename} has been modified")
            self.callback()

def run_on_change():
    print("File changed! Patching...")
    subprocess.run(["python3", "patch_flypy.py"])

if __name__ == "__main__":
    filename = "table.txt"
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