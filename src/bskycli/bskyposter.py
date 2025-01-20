import time

from heapq import heapify, heappop
from pathlib import Path
from time import strptime, mktime
from zipfile import ZipFile

from atproto import Client

import bskycli.config as C
from bskycli.lock import lock
from bskycli.auth import get_credentials


def create_post(timestamp):
    active = C.active_dir()
    queue = C.queue_dir()
    done = C.done_dir()

    zip_name = f'{timestamp}.zip'

    # Move post data to `active` to avoid race conditions if the service is
    # started twice
    with lock():
        (queue / zip_name).rename(active / zip_name)

    z = ZipFile(active / zip_name, 'r')

    blobs = []
    for fname in z.namelist():
        blob = z.read(fname)
        if fname == 'contents':
            text = str(blob, encoding='utf-8')
        else:
            blobs.append(blob)

    client = Client()
    client.login(*get_credentials())

    if len(blobs) == 1:
        client.send_image(text, blobs[0], '')
    else:
        alts = ['' for _ in blobs]
        client.send_images(text, blobs, alts)

    # Finally move posted text and images into `done`
    with lock():
        (active / zip_name).rename(done / zip_name)


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
            break


def main():
    queue = C.queue_dir()

    while True:
        posts = list(queue.glob('*.zip'))
        heapify(posts)

        send_due_posts(posts)

        time.sleep(1)


if __name__ == "__main__":
    main()
