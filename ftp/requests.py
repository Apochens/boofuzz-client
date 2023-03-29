from boofuzz import Request, Session
from .commands import FTPCommand, FTPBody


def make_format_1(command, value) -> Request:
    """<CMD><SP><VAL><CRLF>"""
    return Request(command[0], children=(
        command[1],
        FTPBody.SP,
        value,
        FTPBody.CRLF
    ))


def make_format_2(command) -> Request:
    """<CMD><CRLF>"""
    return Request(command[0], children=(
        command[1],
        FTPBody.CRLF
    ))

def make_format_3(command, value) -> Request:
    """<CMD><L><SP><VAL><R><CRLF>"""
    return Request(command[0], children=(
        command[1],
        FTPBody.left,
        FTPBody.SP,
        value,
        FTPBody.right,
        FTPBody.CRLF
    ))

user = make_format_1(FTPCommand.USER, FTPBody.username)
passw = make_format_1(FTPCommand.PASS, FTPBody.password)
acct = make_format_1(FTPCommand.ACCT, FTPBody.account_information)
cwd = make_format_1(FTPCommand.CWD, FTPBody.pathname)
cdup = make_format_2(FTPCommand.CDUP)
smnt = make_format_1(FTPCommand.SMNT, FTPBody.pathname)
quit = make_format_2(FTPCommand.QUIT)
rein = make_format_2(FTPCommand.REIN)
port = make_format_1(FTPCommand.PORT, FTPBody.host_port)
pasv = make_format_2(FTPCommand.PASV)

type_AE = Request("TYPE-AE", children=(
        FTPCommand.TYPE[1],
        FTPBody.SP,
        FTPBody.type_code_AE,
        FTPBody.CRLF
    ))
type_I = Request("TYPE-I", children=(
        FTPCommand.TYPE[1],
        FTPBody.SP,
        FTPBody.type_code_I,
        FTPBody.CRLF
    ))
type_L = Request("TYPE-L", children=(
        FTPCommand.TYPE[1],
        FTPBody.SP,
        FTPBody.type_code_L,
        FTPBody.CRLF
    ))

stru = make_format_1(FTPCommand.STRU, FTPBody.structure_code)
mode = make_format_1(FTPCommand.MODE, FTPBody.mode_code)
retr = make_format_1(FTPCommand.RETR, FTPBody.pathname)
stor = make_format_1(FTPCommand.STOR, FTPBody.pathname)
stou = make_format_2(FTPCommand.STOU)
appe = make_format_1(FTPCommand.APPE, FTPBody.pathname)

# allo = Request(FTPCommand.ALLO[0], children=(
#     FTPCommand.ALLO[1],
#     FTPBody.SP,
#     FTPBody.decimal_integer,
#     FTPBody.left,
#     FTPBody.SP,
#     FTPBody.R,
#     FTPBody.SP,
#     FTPBody.decimal_integer,
#     FTPBody.right,
#     FTPBody.CRLF
# ))

rest = make_format_1(FTPCommand.REST, FTPBody.marker)
rnfr = make_format_1(FTPCommand.RNFR, FTPBody.pathname)
rnto = make_format_1(FTPCommand.RNTO, FTPBody.pathname)
abor = make_format_2(FTPCommand.ABOR)
dele = make_format_1(FTPCommand.DELE, FTPBody.pathname)
rmd = make_format_1(FTPCommand.RMD, FTPBody.pathname)
mkd = make_format_1(FTPCommand.MKD, FTPBody.pathname)
pwd  = make_format_2(FTPCommand.PWD)
list = make_format_3(FTPCommand.LIST, FTPBody.pathname)
nlst = make_format_3(FTPCommand.NLST, FTPBody.pathname)
site = make_format_1(FTPCommand.SITE, FTPBody.string)
syst = make_format_2(FTPCommand.SYST)
stat = make_format_3(FTPCommand.STAT, FTPBody.pathname)
help = make_format_3(FTPCommand.HELP, FTPBody.string)
noop = make_format_2(FTPCommand.NOOP)


def connect_request(session: Session) -> Session:

    edges = [
        (session.root, user),
        (user, passw),
        (passw, acct),
    ]

    cmd1 = [
        abor, #allo, 
        dele, cwd, cdup, smnt, help, mode, noop, pasv, 
        quit, site, port, syst, stat, rmd, mkd, pwd, stru, type_AE, type_I, type_L
    ]
    for cmd in cmd1:
        edges.append((passw, cmd))

    cmd2 = [
        appe, list, nlst, rein, retr, stor, stou
    ]
    for cmd in cmd2:
        edges.append((passw, cmd))

    edges = edges + [
        (passw, rnfr),
        (rnfr, rnto),
        (passw, rest),
        (rest, appe),
        (rest, stor),
        (rest, retr)
    ]

    # Instantiation
    for (src, dst) in edges:
        print(f'>> Now connecting {dst.name} to {src.name}:{src.id}', end=" ")
        session.connect(src, dst)
        print(f'[Connected {dst.name}:{dst.id}]')

    return session