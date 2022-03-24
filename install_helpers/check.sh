#!/bin/sh

cat /docker-entrypoint.d/20-envsubst-on-templates.sh | grep -q envsubst || (echo "This nginx image does not support templates yet" > /dev/stderr; exit 2)
