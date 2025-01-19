from pathlib import Path

import os
import os.path


BSKY_IMAGES = 4
BSKY_MESSAGE_SIZE = 300


def config_dir():
    cfg_root = (Path(os.environ['XDG_CONFIG_HOME']) if 'XDG_CONFIG_HOME' in os.environ
                else Path(os.environ['HOME']) / '.config' if 'HOME' in os.environ
                else None)

    if cfg_root is None:
        raise RuntimeError('Neither HOME nor XDG_CONFIG_HOME defined, cannot find config directory')

    return cfg_root / 'bskycli'


def data_dir():
    data_root = (Path(os.environ['XDG_DATA_HOME']) if 'XDG_DATA_HOME' in os.environ
                 else Path(os.environ['HOME']) / '.local' / 'share' if 'HOME' in os.environ
                 else None)

    if data_root is None:
        raise RuntimeError('Neither HOME nor XDG_DATA_HOME defined, cannot find config directory')

    return data_root / 'bskycli'


def lock_file():
    return data_dir() / 'LOCK'


def inbox_dir():
    return data_dir() / 'inbox'


def queue_dir():
    return data_dir() / 'queue'


def active_dir():
    return data_dir() / 'active'


def done_dir():
    return data_dir() / 'done'


def setup():
    for d in (config_dir(), data_dir(), inbox_dir(), queue_dir(), active_dir(), done_dir()):
        if d.exists():
            if d.is_dir():
                continue

            raise RuntimeError(f'{d} is not a directory')
        else:
            d.mkdir()

# Guarantee, that the infrastructure directories exist
setup()
