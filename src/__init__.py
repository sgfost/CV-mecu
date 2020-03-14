#! /usr/bin/env python

import argparse
import textwrap
import os
import sys
import subprocess

def test(path):
    #hmm this is probably a bad way to do this.
    # not the easiest thing to make a compliant script to test
    # but oh well it is what it is, it'll work if you have a file
    # that when run, outputs a numeric value (count of eggs)
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
    parser.add_argument('-t',
                        '--test',
                        metavar='PATH',
                        action='store',
                        type=str,
                        help=textwrap.dedent('''\
                        test a counting method
                        PATH is the path to a python file
                        containing a function count()
                        that takes a path to an image and
                        returns a count of eggs
                        '''))

    args = parser.parse_args()

    # do tests
    if args.test:
        test(args.test)

if __name__ == "__main__":
    main()
