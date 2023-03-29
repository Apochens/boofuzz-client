from boofuzz import Delim, Static, String, Group, Block


def make_command(command_name: str) -> String:
    return String('cmd', command_name)


class FTPCommand:
    USER = ("USER", make_command("USER"))
    PASS = ("PASS", make_command("PASS"))
    ACCT = ("ACCT", make_command("ACCT"))
    CWD  = ("CWD", make_command("CWD"))
    CDUP = ("CDUP", make_command("CDUP"))
    SMNT = ("SMNT", make_command("SMNT"))
    QUIT = ("QUIT", make_command("QUIT"))
    REIN = ("REIN", make_command("REIN"))
    PORT = ("PORT", make_command("PORT"))
    PASV = ("PASV", make_command("PASV"))
    TYPE = ("TYPE", make_command("TYPE"))
    STRU = ("STRU", make_command("STRU"))
    MODE = ("MODE", make_command("MODE"))
    RETR = ("RETR", make_command("RETR"))
    STOR = ("STOR", make_command("STOR"))
    STOU = ("STOU", make_command("STOU"))
    APPE = ("APPE", make_command("APPE"))
    ALLO = ("ALLO", make_command("ALLO"))
    REST = ("REST", make_command("REST"))
    RNFR = ("RNFR", make_command("RNFR"))
    RNTO = ("RNTO", make_command("RNTO"))
    ABOR = ("ABOR", make_command("ABOR"))
    DELE = ("DELE", make_command("DELE"))
    RMD  = ("RMD", make_command("RMD"))
    MKD  = ("MKD", make_command("MKD"))
    PWD  = ("PWD", make_command("PWD"))
    LIST = ("LIST", make_command("LIST"))
    NLST = ("NLST", make_command("NLST"))
    SITE = ("SITE", make_command("SITE"))
    SYST = ("SYST", make_command("SYST"))
    STAT = ("STAT", make_command("STAT"))
    HELP = ("HELP", make_command("HELP"))
    NOOP = ("NOOP", make_command("NOOP"))

class FTPBody:
    SP = Delim('space', ' ')
    CRLF = Static('CRLF', '\r\n')
    left = Delim('left', '[')
    right = Delim('right', ']')
    R = String('r', "R")

    username = String('user', 'webadmin')
    password = String('pass', 'ubuntu')
    account_information = String('acct', 'my_account')

    pathname = String('path', "./")
    host_port = String('host_port', '127,0,0,1,3000,3001')

    type_code_AE = Block("type-code-AE", children=(
        Group('typecode', values=['A', "E"]),
        left,
        SP,
        Group('form-code', values=['N', 'T', 'C']),
        right
    ))
    type_code_I = Block('type-code-I', children=(
        String('type-code-I', 'I')
    ))
    type_code_L = Block('type-code-L', children=(
        String('type', 'L'),
        SP,
        String('byte-size', '20')
    ))

    structure_code = Group('structure-code', values=[code for code in 'FRP'])
    mode_code = Group('mode-code', values=[code for code in 'SBC'])
    
    decimal_integer = String('decimal-integer', "1000")
    marker = String('marker', 'abcd')

    string = String('string', 'syst')