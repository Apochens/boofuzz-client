from boofuzz import *
from ftp import connect_request

if __name__ == '__main__':
    session = Session(
        target=Target(
            connection=TCPSocketConnection('127.0.0.1', 2200)
        ),
        fuzz_db_keep_only_n_pass_cases=10
    )
    connect_request(session)
    session.fuzz()