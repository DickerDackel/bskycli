import os.path

from atproto import SessionEvent

import bskycli.config as C

from bskycli.config import config_dir


def get_credentials():
    credentials_file = os.path.join(config_dir(), 'credentials')

    with open(credentials_file) as f:
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
        os.chmod(session_file.fileno(), 0o600)
        f.write(session)


def session_change(event, session):
    print(f'Session changed: {event=} - {session=}')
    if event in (SessionEvent.CREATE, SessionEvent.REFRESH):
        save_session(session)


def login(client):
    client.on_session_change(session_change)

    if session := get_session():
        print('Reusing existing session')
        client.login(session_string=session)
    else:
        print('New login')
        client.login(*get_credentials())

__all__ = [
    get_credentials,
]
