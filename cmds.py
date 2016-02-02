import subprocess
import os


def cmd_hello(args):
    return 'HELLO'


def cmd_cmds(args):
    return '\n'.join(COMMANDS.keys())


def cmd_cpu_load(args):
    return subprocess.check_output('uptime').split()[-3].replace(',', '')


def cmd_cpu_idle(args):
    return subprocess.check_output('vmstat').splitlines()[-1].split()[-1]


def cmd_mem_free(args):
    return subprocess.check_output('vmstat').splitlines()[-1].split()[3]


def cmd_cpu_temp(args):
    return subprocess.check_output(('sysctl', '-n', 'hw.sensors.cpu0.temp0'))


def cmd_fan_speeds(args):
    return subprocess.check_output(('sysctl', '-n', 'hw.sensors.ipmi0.fan'))


def cmd_system_temp(args):
    return subprocess.check_output(('sysctl', '-n', 'hw.sensors.ipmi0.temp'))


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


# this must be at the bottom
COMMANDS = {name[4:]: func for name, func in globals().items()
            if callable(func) and name.startswith('cmd_')}
