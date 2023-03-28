from boofuzz import *

pre_send_callbacks = []

post_test_case_callbacks = []

post_start_target_callbacks = []

loggers = []

session = Session(
    target=Target(
        connection=TCPSocketConnection('127.0.0.1', 2200)
    ),
    fuzz_db_keep_only_n_pass_cases=5,
)


USERNAME = String("username", "webadmin")
PASSWORD = String("val", "ubuntu")


SP = Delim('space', ' ')
CRLF = Static('end', "\r\n")
PATHNAME = String('pathname', ".")


user = Request("user", children=(String("command", "USER"), SP, USERNAME, CRLF))
passw = Request("pass", children=(String("key", "PASS"), SP, PASSWORD, CRLF))

stor = Request("stor", children=(String("key", "STOR"), SP, String("val", "AAAA"),CRLF))
retr = Request("retr", children=(String("key", "RETR"), SP, String("val", "AAAA"), CRLF))

# Account
acct = Request("acct", children=(String('key', "ACCT"), Delim('space', " "), String('value', "AAAA"), CRLF))
# CWD
cwd = Request("cwd", children=(String('key', 'CWD'), SP, String("value", "."), CRLF))
# CDUP: Back to outer dir
# SMNT
# REIN
# QUIT

session.connect(user)
session.connect(user, passw)
session.connect(passw, stor)
session.connect(passw, retr)


if __name__ == '__main__':
    session.fuzz()