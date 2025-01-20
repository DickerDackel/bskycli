import argparse
import sys
import time

from pathlib import Path

from bskycli.post import post

def main():
    now = time.strftime('%F-%T')

    cmdline = argparse.ArgumentParser(description='Schedule a bluesky posts')
    cmdline.add_argument('-t', '--at', type=str, default=now, help='Earliest time to post.  Format is YYYY-MM-DD-HH:MM[:SS].  Default is now.')
    cmdline.add_argument('textfile', type=Path, help='File containing the post text.  Use "-" for stdin.')
    cmdline.add_argument('images', nargs='*', type=Path, help='Optional list of up to 4 images')

    opts = cmdline.parse_args(sys.argv[1:])

    post(opts)


if __name__ == "__main__":
    main()
