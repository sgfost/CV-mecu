#! /usr/bin/env python

import argparse
import textwrap
# For relative imports to work in Python 3.6
# import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import os
import sys
import subprocess

from observer import start
import smartcount

# default backend
backend = ""

# run on a single file
def run_on_file(backend, path):
    if backend == "smartcount":
        print(smartcount.count(path))

# run in the background, monitoring path for new files
def run_in_background(backend, path):
    if backend == "smartcount":
        print(f"Monitoring {path} for new files to analyze..")
        start(["*"], path, False)


def main():
    # print example usage
    examples = '''
example usage:
  # (run in the background monitoring data/
  #  directory relative to the current)
  python cpv.py -a smartcount -b ./data/

  # (run on a single file called eggs.png
  #  in the current directory)
  python cpv.py -a smartcount -f eggs.png
    '''

    # create parser
    parser = argparse.ArgumentParser(description='Count mosquito eggs in an image',
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     epilog=examples)
    # add args
    parser.add_argument('-a',
                        '--backend',
                        metavar='NAME',
                        action='store',
                        type=str,
                        help=textwrap.dedent('''\
                        use a specific backend algorithm
                        available backends:
                         - smartcount
                        '''))
    parser.add_argument('-f',
                        '--file',
                        metavar='PATH',
                        action='store',
                        type=str,
                        help=textwrap.dedent('''\
                        run on a single file and print
                        the count
                        '''))
    parser.add_argument('-b',
                        '--background',
                        metavar='PATH',
                        action='store',
                        type=str,
                        help=textwrap.dedent('''\
                        run in the background, observe PATH
                        for new files and run on files
                        '''))

    args = parser.parse_args()
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(0)



    # arg logic
    if args.backend:
        # set backend to specified
        backend = args.backend
    else: # default to smartcount backend
        backend = "smartcount"
    # check for valid backend
    if backend == "smartcount": # || backend == "modeldetect"
        if args.file:
            if os.path.isfile(args.file):
                run_on_file(backend, args.file)
            else:
                print(f"Error: {args.file} does not exist or is a directory")

        if args.background:
            if os.path.isdir(args.background):
                run_in_background(backend, args.background)
            else:
                print(f"Error: {args.background} is not a directory")
        
    elif backend == "modeldetect":
        #TODO: integrate monica's object detection counting
        print("doesnt exist yet, whoops")
    else:
        print(f"Error: {backend} is not a valid backend")

if __name__ == "__main__":
    main()
