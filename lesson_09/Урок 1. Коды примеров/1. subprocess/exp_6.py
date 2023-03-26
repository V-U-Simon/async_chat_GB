"""Пинг ресурса"""

from subprocess import Popen, PIPE


def ping_ip(ip_address):
    """
    Ping IP address and return tuple:
    On success:
        * True
        * command output (stdout)
    On failure:
        * False
        * error output (stderr)
    """
    args = ['ping', ip_address]
    reply = Popen(args, stdout=PIPE, stderr=PIPE)

    print(reply)
    CODE = reply.wait()
    if CODE == 0:
        return True, reply.stdout
    else:
        return False, reply.stderr


print(ping_ip('192.168.1.2'))
print(ping_ip('a'))
