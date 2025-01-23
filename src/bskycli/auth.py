import os.path

from time import localtime

from atproto import SessionEvent
from atproto.exceptions import RequestException

import bskycli.config as C

from bskycli.config import config_dir


def get_credentials():
    credentials_file = config_dir() / 'credentials'

    with credentials_file.open() as f:
        user, password = f.readline().strip().split(':')
        return user, password


def get_session():
    session_file = C.data_dir() / 'session.txt'
    try:
        with session_file.open() as f:
            return f.read()
    except FileNotFoundError:
        return None


def save_session(session):
    session_file = C.data_dir() / 'session.txt'
    with session_file.open('w') as f:
        os.chmod(f.fileno(), 0o600)
        f.write(session)


def session_change(event, session):
    print(f'Session changed: {event=} - {session=}')
    if event in (SessionEvent.CREATE, SessionEvent.REFRESH):
        save_session(session.export())


def login(client):
    client.on_session_change(session_change)

    try:
        if session := get_session():
            print('Reusing existing session')
            client.login(session_string=session)
        else:
            print('New login')
            client.login(*get_credentials())
    except RequestException as e:
        if e.content.error  == 'RateLimitExceeded':
            reset_time = localtime(e.headers['ratelimit-reset'])
            policy = e.headers['ratelimit-policy']
            raise SystemExit(f'{e.content.message} - Retry {reset_time}  Polocy: {policy}')
        else:
            print('Haven\'t had this exception yet...')
            raise e


__all__ = [
    get_credentials,
]
