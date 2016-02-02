import subprocess

def cmd_hello(args):
    return 'HELLO'


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


# this must be at the bottom
COMMANDS = {name[4:]: func for name, func in globals().items()
            if callable(func) and name.startswith('cmd_')}
