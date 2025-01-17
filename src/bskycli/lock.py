from contextlib import contextmanager
from fcntl import flock, LOCK_EX, LOCK_UN

from bskycli.config import lock_file

@contextmanager
def lock():
    with open(lock_file(), 'a') as f:
        try:
            flock(f.fileno(), LOCK_EX)
            yield f
        finally:
            flock(f.fileno(), LOCK_UN)
