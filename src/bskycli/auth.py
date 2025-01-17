import os.path

from bskycli.config import config_dir


def get_credentials():
    credentials_file = os.path.join(config_dir(), 'credentials')

    with open(credentials_file) as f:
        user, password = f.readline().strip().split(':')
        return user, password


__all__ = [
    get_credentials,
]
