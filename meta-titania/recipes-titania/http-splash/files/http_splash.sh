#!/bin/sh

# Skip everything
while /bin/true; do
  read line <&3
  [ "$line" == $'\r' ] && break;
done

# SystemD passes fd3 for communication
SPLASH_FILE="/usr/share/http-splash/http-splash.html"

# Headers
# TODO: drop a 404 if html not found, but this is real paranoid
cat >&3 <<EOF
HTTP/1.0 200 OK
Content-Type: text/html
Content-Length: $(wc -c $SPLASH_FILE | cut -f1 -d' ')
Date: $(date -R)
EOF

echo >&3

# Content
cat $SPLASH_FILE >&3

# Waiting for the other side to close
read line <&3

