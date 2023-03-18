from messenger.config import DEFAULT_IP, DEFAULT_PORT
from loguru import logger
import argparse
from messenger import Client, Server

logger.level = "DEBUG"


@logger.catch()
def main():

    # Create the top-level parser
    parser = argparse.ArgumentParser(description='My CLI')
    menu_parsers = parser.add_subparsers()

    # common commands
    parser.add_argument('-ip', '--ip', default=DEFAULT_IP, help=f'custom server ip, like "localhost" or "127.0.0.1". Default: {DEFAULT_IP}')
    parser.add_argument('-p', '--port', default=DEFAULT_PORT, help=f'custom server port, like "8342". Default: {DEFAULT_PORT}')
    parser.add_argument('-a', '--address', help='cuistom server address, like "localhost:8893"')

    # server-side commands
    server_parser = menu_parsers.add_parser('server', help='run server')
    server_parser.add_argument('server', help='run server', action='store_true', default=False)

    # client-side commands
    client_parser = menu_parsers.add_parser('client', help='client side commands: -m, -to, -u, -pw')
    client_parser.add_argument('-m', '--message', help='Message to send', default='Hello!')
    client_parser.add_argument('-to', '--to', help='destination of message')
    client_parser.add_argument('-u', '--user', help='User name')
    client_parser.add_argument('-pw', '--password', help='User password')

    # Parse the command line arguments
    args = parser.parse_args()

    args.address = (args.ip, args.port) if not args.address else args.address
    logger.debug(args)

    if getattr(args, 'server', False):
        logger.debug('try to run server')
        server = Server(*args.address)
        server.run()
    else:
        logger.debug('try to run client')
        client = Client(*args.address)
        client.run()


if __name__ == "__main__":
    main()
