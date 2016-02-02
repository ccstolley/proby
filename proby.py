import daemonize
import logging
try:
    from socketserver import StreamRequestHandler, ThreadingTCPServer
except ImportError:
    from SocketServer import StreamRequestHandler, ThreadingTCPServer
from cmds import COMMANDS


logging.basicConfig(filename='/tmp/proby.log', level=logging.DEBUG)
log = logging.getLogger()


def default_cmd(args):
    """
    Return a default response when an unknown command is specified.
    """
    return 'UNKNOWN_COMMAND'


def parse_command(line):
    """
    Determine the command and dispatch the proper handler function.
    """
    tokens = line.split()
    cmd, args = tokens[0], tokens[1:]
    try:
        log.info("%s: %s", cmd, args)
        return COMMANDS.get(cmd, default_cmd)(args)
    except Exception as e:
        log.error("%s: %s", cmd, e)
        return 'error'


def main():
    """
    Create and start server.
    """
    server = ThreadingTCPServer(('', 7000), ProbeHandler)
    server.serve_forever()


class ProbeHandler(StreamRequestHandler):
    def handle(self):
        for line in self.rfile:
            log.debug(line)
            response = parse_command(line)
            self.wfile.write('{}\n'.format(response))
            return  # one cmd per connection

    def handle_error(self, request, client_address):
        log.exception("%s: %s", request, client_address)


if __name__ == '__main__':
    daemonize.daemon_main(main)
