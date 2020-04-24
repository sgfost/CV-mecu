import sys
import os
import time
import datetime
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import smartcount

class backend(object):
    def __init__(self, value): self.value = value

bend = backend("default")

# default event handler, prints out the time of creation and the file
def on_created(event):
    # wait until the filesize stops growing, to make sure we
    # arent analyzing halfway uploaded image
    filesize = -1
    while (filesize != os.path.getsize(event.src_path)):
        filesize = os.path.getsize(event.src_path)
        time.sleep(1)

    now = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{now}]\t\t{event.src_path} detected")

    # count with smartcount
    count = smartcount.count(event.src_path)
    # write to file
    head, countsfilename = os.path.split(event.src_path)
    for i, c in enumerate(countsfilename):
        if c == '.':
            countsfilename = countsfilename[:i] + '_' + countsfilename[i+1:]
    countsfilename += "_count.txt"
    countsfilename = os.path.join(head, countsfilename)
    countsfile = open(countsfilename, 'x')
    countsfile.write(str(count))
    countsfile.close()

    print(f"{count} eggs counted, written to {countsfilename}")
    print("----------------------------------------------------")

# start observing, pass False if no custom handler
def start(patterns, path, new_backend):
    bend.value = new_backend
    # ignore txt extensions so we don't run on the generated count file
    # TODO: more robust error handling when we dont get an image file
    ignore_patterns = ["*.txt"]
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
    start("*", sys.argv[1], False)
