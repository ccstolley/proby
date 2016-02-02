Proby - a system probe
==

Proby is a daemon that responds to simple text commands to provide
system information. This is especially useful for monitoring services
such as Argus or Nagios.

Proby has no dependencies besides Python 2 or 3.

Proby commands can be easily created or modified.

Example Usage
--

```
# start the daemon
$ python ./proby start

# send a command
$ printf "cpu_load\n" | nc localhost 7000
0.42
$ printf "mem_free\n" | nc localhost 7000
2564492
$ printf "hello\n" | nc localhost 7000
HELLO
```
