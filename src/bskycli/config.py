import os
import os.path


BSKY_IMAGES = 4
BSKY_MESSAGE_SIZE = 300


def config_dir():
    cfg_root = (os.environ['XDG_CONFIG_HOME'] if 'XDG_CONFIG_HOME' in os.environ
               else os.path.join(os.environ['HOME'], '.config') if 'HOME' in os.environ
               else None)

    if cfg_root is None:
        raise RuntimeError('Neither HOME nor XDG_CONFIG_HOME defined, cannot find config directory')

    return os.path.join(cfg_root, 'bskycli')


def data_dir():
    data_root = (os.environ['XDG_DATA_HOME'] if 'XDG_DATA_HOME' in os.environ
                 else os.path.join(os.environ['HOME'], '.local', 'share') if 'HOME' in os.environ
                 else None)

    if data_root is None:
        raise RuntimeError('Neither HOME nor XDG_DATA_HOME defined, cannot find config directory')

    return os.path.join(data_root, 'bskycli')


def lock_file():
    return os.path.join(data_dir(), 'LOCK')


def inbox_dir():
    return os.path.join(data_dir(), 'inbox')


def queue_dir():
    return os.path.join(data_dir(), 'queue')


def active_dir():
    return os.path.join(data_dir(), 'active')


def done_dir():
    return os.path.join(data_dir(), 'done')


def setup():
    for d in (config_dir(), data_dir(), inbox_dir(), queue_dir(), active_dir(), done_dir()):
        if os.path.exists(d):
            if os.path.isdir(d):
                continue

            raise RuntimeError(f'{d} is not a directory')
        else:
            os.mkdir(d)

# Guarantee, that the infrastructure directories exist
setup()
