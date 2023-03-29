from boofuzz import *
from .ftp.requests import connect_request


if __name__ == '__main__':
    session = Session(
        target=Target(
            connection=TCPSocketConnection('127.0.0.1', 2200)
        ),
    )

    connect_request(session)
    session.fuzz()