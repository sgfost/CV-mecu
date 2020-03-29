#! /usr/bin/env python

import argparse
import textwrap
# For relative imports to work in Python 3.6
# import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import os
import sys
import subprocess

from observer import start

# default backend
backend = "pixelcounting"

# TODO: phase this out
def test(path):
    command = ["python"]
    command.append(path)
    imagelist = os.listdir('../data/images')
    imagecounts = [line.rstrip('\n') for line in open('../data/counts.txt')]
    currimg = 0
    for image in imagelist:
        command.append('../data/images/' + image)
        count = int(subprocess.check_output(command))
        print('Percent difference for test #' + str((currimg + 1)) + ':')
        print(abs(count - int(imagecounts[currimg])) / int(imagecounts[currimg]) * 100)
        currimg += 1


def main():
    # create parser
    parser = argparse.ArgumentParser(description='Count mosquito eggs in an image',
                                     formatter_class=argparse.RawTextHelpFormatter)
    # add args
    parser.add_argument('file_path',
                        metavar='PATH',
                        action='store',
                        type=str,
                        nargs='?',
                        help='Path of file to run counter on')
    # TODO: phase this out
    parser.add_argument('-t',
                        '--test',
                        metavar='PATH',
                        action='store',
                        type=str,
                        help=textwrap.dedent('''\
                        test a counting method <PATH>.py
                        '''))
    parser.add_argument('-a',
                        '--backend',
                        metavar='NAME',
                        action='store',
                        type=str,
                        help=textwrap.dedent('''\
                        use a specific backend algorithm
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

    # arg logic
    if args.backend:
        # set backend to specified
        backend = args.backend

    if args.test:
        test(args.test)
    elif args.background:
        # start running in background
        print(f"watching {args.background} for new images")
        patterns = ["*.png", "*.jpg"]
        print(f"using backend {args.backend}")
        start(patterns, args.background, backend)
    else:
        # assume user wants to run on a single file
        # run on a single file with PATH positional argument
        print(args.file_path)


if __name__ == "__main__":
    main()
