import time

from heapq import heapify, heappop
from pathlib import Path
from time import strptime, mktime

from atproto import Client

import bskycli.config as C
from bskycli.lock import lock
from bskycli.auth import get_credentials


def create_post(timestamp):
    active = C.active_dir()
    queue = C.queue_dir()
    done = C.done_dir()

    text_file = f'{timestamp}.txt'
    images = [f.name for f in queue.glob(f'{timestamp}*') if f.name != text_file]

    # Move post data to `active` to avoid race conditions if the service is
    # started twice
    with lock():
        (queue / text_file).rename(active / text_file)
        for img in images:
            (queue / img).rename(active / img)

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
        (active / text_file).rename(done / text_file)
        for img in images:
            (active / img).rename(done / img)


def send_due_posts(posts):
    while posts:
        now = int(time.time())

        newest = Path(heappop(posts))

        timestamp = newest.stem
        fmt = '%Y-%m-%d-%H:%M' if len(timestamp) == 16 else '%Y-%m-%d-%H:%M:%S'
        time_struct = strptime(timestamp, fmt)
        time_val = mktime(time_struct)

        if time_val < now:
            print(f'Posting {timestamp}')
            create_post(timestamp)
        else:
            print(f'Next post due at {timestamp}')
            break


def main():
    queue = C.queue_dir()

    while True:
        posts = list(queue.glob('*.txt'))
        heapify(posts)

        send_due_posts(posts)

        time.sleep(1)


if __name__ == "__main__":
    main()
