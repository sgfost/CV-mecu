# CV-mecu

```
usage: cpv.py [-h] [-a NAME] [-f PATH] [-b PATH]

Count mosquito eggs in an image

optional arguments:
  -h, --help            show this help message and exit
  -a NAME, --backend NAME
                        use a specific backend algorithm
                        available backends:
                         - smartcount
  -f PATH, --file PATH  run on a single file and print
                        the count
  -b PATH, --background PATH
                        run in the background, observe PATH
                        for new files and run on files

example usage:
  # (run in the background monitoring data/
  #  directory relative to the current)
  python cpv.py -a smartcount -b ./data/

  # (run on a single file called eggs.png
  #  in the current directory)
  python cpv.py -a smartcount -f eggs.png
```
