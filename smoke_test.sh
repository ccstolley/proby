#!/bin/sh
# Simple test script to check if probes work
tests_ok=1
commands=$(printf "cmds\n"| nc localhost 7000)

if [ X"$commands" = X ]; then
    echo "Proby is not running"
    exit 1
fi

for cmd in $commands; do
    val=$(printf "%s\n" "$cmd" | nc localhost 7000)
    if [ X"$val" = X -o X"$val" = Xerror ]; then
        echo "$cmd is broken"
        tests_ok=0
    fi
done

if [ $tests_ok = 1 ]; then
    echo "Tests OK"
fi
