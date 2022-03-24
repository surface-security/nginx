#!/bin/sh

set -ex
PLATFORM="$1"
URL="https://github.com/fopina/confgen/releases/download/v0.1.2/confgen_"

if [[ "$PLATFORM" == linux/arm64 ]]; then
    MACH=linux_arm64
elif [[ "$PLATFORM" == linux/arm/* ]]; then
    MACH=linux_arm
else
    MACH=linux_amd64
fi

curl -L ${URL}sprig_${MACH} -o /usr/bin/confgen
chmod a+x /usr/bin/confgen
