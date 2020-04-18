import sys
import os
import time
import datetime
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from process import count

# shitty workaround this will change when we implement
# the actual backend algorithms
class backend(object):
    def __init__(self, value): self.value = value

bend = backend("default")

# default event handler, prints out the time of creation and the file
def on_created(event):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{now}]\t{event.src_path} created")
    count(event.src_path, bend.value)

# start observing, pass False if no custom handler
def start(patterns, path, new_backend):
    bend.value = new_backend
    ignore_patterns = ""
    ignore_directories = False
    case_sensitive = True
    handler = PatternMatchingEventHandler(patterns, ignore_patterns,
                                          ignore_directories, case_sensitive)
    handler.on_created = on_created
    observer = Observer()
    observer.schedule(handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

backend = ""

if __name__ == "__main__":
    start("*", "/home/me/testdir", False)
