#!/bin/sh
# Simple test script to check if probes work
tests_ok=1

for cmd in `printf "cmds\n"| nc localhost 7000`; do
    val=$(printf "$cmd\n"| nc localhost 7000)
    if [ X"$val" = X -o X"$val" = Xerror ]; then
        echo "$cmd is broken"
        tests_ok=0
    fi
done

if [ $tests_ok ]; then
    echo "Tests OK"
fi
