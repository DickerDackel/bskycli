import argparse
import os.path
import re
import sys
import time

from pathlib import Path
from shutil import copyfile, move

import bskycli.config as C
from bskycli.lock import lock

RX = re.compile(r'^\d{4}-\d{2}-\d{2}-\d{2}:\d{2}(:\d{2})?$')

def main():
    now = time.strftime('%F-%T')

    cmdline = argparse.ArgumentParser(description='Schedule a bluesky posts')
    cmdline.add_argument('-t', '--at', type=str, default=now, help='Earliest time to post.  Format is YYYY-MM-DD-HH:MM:SS.  Default is now.')
    cmdline.add_argument('textfile', type=Path, help='File containing the post text.  Use "-" for stdin.')
    cmdline.add_argument('images', nargs='*', type=Path, help='Optional list of up to 4 images')

    opts = cmdline.parse_args(sys.argv[1:])

    if re.fullmatch(RX, opts.at) is None:
        raise SystemExit(f'Time format of {opts.at} is invalid')

    if len(opts.images) > C.BSKY_IMAGES:
        raise SystemExit(f'Bluesky only allows {C.BSKY_IMAGES} per post')

    with open(opts.textfile) if str(opts.textfile) != '-' else sys.stdin as f:
        text = f.read()

    if len(text) > 300:
        raise SystemExit(f'Bluesky only allows posts up to {C.BSKY_MESSAGE_SIZE} characters')


    # This whole shit is the usual email server problem.  The files must not
    # be handled while they are still added.
    #
    # 1. Add them to the inbox
    # 2. Aquire a lock to move them into the actual queue.  A move is an
    #    atomic operation, but we're moving up to 5 files, so a task switch
    #    could occur.  That's what the lock is for.  But doing it only here
    #    makes sure, the blocking of the server is minimal.
    # 3. Move the created files from the inbox into the queue
    # 4. Release the lock.

    inbox = Path(C.inbox_dir())
    queue = Path(C.queue_dir())

    post_files = []

    post_files.append(inbox / f'{opts.at}.txt')
    with open(post_files[-1], 'w') as f:
        print(text, file=f)

    for i, img in enumerate(opts.images):
        post_files.append(inbox / f'{opts.at}-{i}{img.suffix}')

        copyfile(img, post_files[-1])

    with lock():
        for f in post_files:
            move(f, queue)


if __name__ == "__main__":
    main()
