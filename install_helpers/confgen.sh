#!/bin/sh

set -ex

PLATFORM="$1"
SPRIG="$2"

URL="https://github.com/fopina/confgen/releases/download/v0.1.2/confgen_"

if [[ "$PLATFORM" == linux/arm64 ]]; then
    MACH=linux_arm64
elif [[ "$PLATFORM" == linux/arm/* ]]; then
    MACH=linux_arm
else
    MACH=linux_amd64
fi

if [ "$SPRIG" == "1" ]; then
    SPRIG="sprig_"
else
    SPRIG=""
fi

curl --fail -L ${URL}${SPRIG}${MACH} -o /usr/bin/confgen
chmod a+x /usr/bin/confgen
