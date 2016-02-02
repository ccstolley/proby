"""
Module for creating daemon processes.
"""
from __future__ import print_function
import os
import sys
import signal
import atexit


def daemonize(pidfile, stdin='/dev/null', stdout='/dev/null',
              stderr='/dev/null'):
    """
    Convert current process to a daemon on unix-like systems.
    """
    if os.path.exists(pidfile):
        raise RuntimeError("Already running.")

    # detach from parent
    if os.fork() > 0:
        raise SystemExit

    os.chdir('/')
    os.umask(0)
    os.setsid()

    # relinquish session leadership
    if os.fork() > 0:
        raise SystemExit

    sys.stdout.flush()
    sys.stderr.flush()
    with open(stdin, 'rb', 0) as fobj:
        os.dup2(fobj.fileno(), sys.stdin.fileno())
    with open(stdout, 'ab', 0) as fobj:
        os.dup2(fobj.fileno(), sys.stdout.fileno())
    with open(stderr, 'ab', 0) as fobj:
        os.dup2(fobj.fileno(), sys.stderr.fileno())

    with open(pidfile, 'w') as fobj:
        fobj.write(str(os.getpid()))
    atexit.register(lambda: os.remove(pidfile))

    def sigterm_handler(signo, frame):
        raise SystemExit(1)
    signal.signal(signal.SIGTERM, sigterm_handler)


def daemon_main(main_func, argv=None, pidfile=None):
    """
    Defines a main function for controlling the daemon.

    :param main_func: callable that starts application
    :param argv: arguments, defaults to sys.argv
    :param pidfile: pid file, defaults to /tmp/<prog name>
    """
    if argv is None:
        argv = sys.argv
    if pidfile is None:
        pidfile = '/tmp/{}.pid'.format(argv[0])

    if len(argv) < 2 or argv[1] not in ('start', 'stop'):
        print("Usage: {} [start|stop]".format(argv[0]))
        raise SystemExit(1)

    if argv[1] == 'start':
        daemonize(pidfile)
        main_func()
    elif argv[1] == 'stop':
        if os.path.exists(pidfile):
            with open(pidfile) as fobj:
                os.kill(int(fobj.read()), signal.SIGTERM)
        else:
            print("Not running")
            raise SystemExit(1)
    else:
        print("Unknown command")
        raise SystemExit(1)
