import subprocess
import os
from functools import partial


def cmd_hello(args):
    return 'HELLO'


def cmd_cmds(args):
    return '\n'.join(sorted(COMMANDS.keys()))


def cmd_cpu_load(args):
    return _shell_exec('uptime').split()[-3].replace(',', '')


def cmd_cpu_idle(args):
    return _shell_exec('vmstat').splitlines()[-1].split()[-1]


def cmd_mem_free(args):
    if _platform() == "darwin":
        return _shell_exec('vm_stat').splitlines()[1].split()[2].strip('.')
    else:
        return _shell_exec('vmstat').splitlines()[-1].split()[4]

def cmd_cpu_temp(args):
    return _shell_exec(('sysctl', '-n', 'hw.sensors.cpu0.temp'))


def cmd_fan_speeds(args):
    return _shell_exec(('sysctl', '-n', 'hw.sensors.ipmi0.fan'))


def cmd_system_temp(args):
    funcs = (partial(_shell_exec, ('sysctl', '-n', 'hw.sensors.ipmi0.temp')),
             partial(_shell_exec, ('sysctl', '-n', 'hw.sensors.acpitz0.temp')))
    for f in funcs:
        r = f()
        if r:
            return r


def _disk_free(mount_point):
    s = os.statvfs(mount_point)
    return round(float(s.f_bavail * s.f_frsize) /
                 float(s.f_blocks * s.f_frsize), 3)

def cmd_disk_usage_root(args):
    return _disk_free('/')


def cmd_disk_usage_var(args):
    return _disk_free('/var')


def cmd_disk_usage_home(args):
    return _disk_free('/home')


def cmd_disk_usage_tmp(args):
    return _disk_free('/tmp')


def cmd_platform(args):
    return _platform()


def _platform():
    return os.uname()[0].lower()


def _shell_exec(args):
    return subprocess.check_output(args).decode('utf-8')

# this must be at the bottom
COMMANDS = {name[4:]: func for name, func in globals().items()
            if callable(func) and name.startswith('cmd_')}
