import re
import sys

from pathlib import Path
from zipfile import ZipFile

import bskycli.config as C

from bskycli.lock import lock


RX = re.compile(r'^\d{4}-\d{2}-\d{2}-\d{2}:\d{2}(:\d{2})?$')


def post(opts):
    # This whole shit is the usual email server problem.  The files must not
    # be handled while they are still added.
    # That can be achieved 
    #
    # 1. Add them to the inbox
    # 2. Aquire a lock to move them into the actual queue.  A move is an
    #    atomic operation, but we're moving up to 5 files, so a task switch
    #    could occur.  That's what the lock is for.  But doing it only here
    #    makes sure, the blocking of the server is minimal.
    # 3. Move the created files from the inbox into the queue
    # 4. Release the lock.
    inbox = C.inbox_dir()
    queue = C.queue_dir()

    zip_name = f'{opts.at}.zip'
    z = ZipFile(inbox / zip_name, 'w')

    if re.fullmatch(RX, opts.at) is None:
        raise SystemExit(f'Time format of {opts.at} is invalid')

    if len(opts.images) > C.BSKY_IMAGES:
        raise SystemExit(f'Bluesky only allows {C.BSKY_IMAGES} per post')

    with open(opts.textfile) if str(opts.textfile) != '-' else sys.stdin as f:
        text = f.read()

    if len(text) > 300:
        raise SystemExit(f'Bluesky only allows posts up to {C.BSKY_MESSAGE_SIZE} characters')

    z.writestr('contents', text)

    for i, fname in enumerate(opts.images):
        with open(fname, 'rb') as f:
            image = f.read()
            z.writestr(f'image-{i}{fname.suffix}', image)

    z.close()

    with lock():
        (inbox / zip_name).rename(queue / zip_name)
