import time

from glob import glob
from heapq import heapify, heappop
from pathlib import Path
from shutil import move
from time import strptime, mktime

from atproto import Client

import bskycli.config as C
from bskycli.lock import lock
from bskycli.auth import get_credentials


def create_post(timestamp):
    active = Path(C.active_dir())
    queue = Path(C.queue_dir())
    done = Path(C.done_dir())

    text_file = f'{timestamp}.txt'
    images = [f.name for f in queue.glob(f'{timestamp}*') if f.name != text_file]

    # Move post data to `active` to avoid race conditions if the service is
    # started twice
    with lock():
        move(queue / text_file, active / text_file)
        for img in images:
            move(queue / img, active / img)

    with open(active / text_file) as f:
        text = f.read().strip()

    blobs = []
    for img in images:
        with open(active / img, 'rb') as f:
            blobs.append(f.read())

    client = Client()
    client.login(*get_credentials())

    if len(blobs) == 1:
        client.send_image(text, blobs[0], '')
    else:
        alts = ['' for _ in blobs]
        client.send_images(text, blobs, alts)

    # Finally move posted text and images into `done`
    with lock():
        move(active / text_file, done / text_file)
        for img in images:
            move(active / img, done / img)


def send_due_posts(posts):
    while posts:
        now = int(time.time())

        newest = Path(heappop(posts))

        timestamp = newest.name.rstrip('.txt')
        time_struct = strptime(timestamp, '%Y-%m-%d-%H:%M')
        time_val = mktime(time_struct)

        if time_val < now:
            print(f'Posting {timestamp}')
            create_post(timestamp)
        else:
            print(f'Next post due at {timestamp}')
            break


def main():
    queue = Path(C.queue_dir())
    active = Path(C.active_dir())
    done = Path(C.done_dir())

    while True:
        posts = list(queue.glob('*.txt'))
        heapify(posts)

        send_due_posts(posts)

        time.sleep(1)


if __name__ == "__main__":
    main()
