#!/usr/bin/env python3
# coding: utf-8

import argparse

from animwal.animate import Animate
from animwal.helpers import extract_from_gif

def main():
    parser = argparse.ArgumentParser(description='animated wallpapers')

    parser.add_argument(
        '-a', '--animate',
        metavar=('path', 'time'), nargs=2,
        help='animate image files placed in `path` every `time` ms.'
    )

    parser.add_argument(
        '-g', '--generate',
        metavar=('gif-file', 'output'), nargs=2,
        help='extract frames from given `gif-file` to `output` folder.'
    )

    args = parser.parse_args()

    if args.generate:
        print ('animwal extraced {} frame(s) from {} to {}.'.format(
            extract_from_gif(*args.generate),
            *args.generate))

    elif args.animate:
        engine = Animate(*args.animate)
        engine.mainloop()

    else:
        parser.print_help()

if __name__ == '__main__':
    main()