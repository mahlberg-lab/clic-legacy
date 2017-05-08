#!/bin/sh
set -ex

# This script will create a systemd unit for running CLiC uWSGI, and
# an nginx config.
#
# It is tested on Debian, but should hopefully work on anything systemd-based.

CLIC_PATH="$(dirname "$(readlink -f "$0")")"
SERVICE_NAME="${SERVICE_NAME-clic}"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
SERVER_NAME="${SERVER_NAME-clic.bham.ac.uk}"
UWSGI_BIN="${CLIC_PATH}/bin/uwsgi"
UWSGI_USER="${UWSGI_USER-nobody}"
UWSGI_GROUP="${UWSGI_GROUP-nogroup}"
UWSGI_SOCKET=/tmp/${SERVICE_NAME}_uwsgi.sock
UWSGI_TIMEOUT="${UWSGI_TIMEOUT-5m}"

# ---------------------------

[ -f "${CLIC_PATH}/secret-secretkey.txt" ] || dd if=/dev/random bs=20 count=1 | sha256sum | cut -f1 -d' ' > "${CLIC_PATH}/secret-secretkey.txt"

[ -f "${CLIC_PATH}/clic-chapter-cache.pickle" ] || touch "${CLIC_PATH}/clic-chapter-cache.pickle"
chown ${UWSGI_USER} "${CLIC_PATH}/clic-chapter-cache.pickle"
chmod g+w "${CLIC_PATH}/clic-chapter-cache.pickle"

# ---------------------------

systemctl | grep -q "${SERVICE_NAME}.service" && systemctl stop ${SERVICE_NAME}.service
cat <<EOF > ${SERVICE_FILE}
[Unit]
Description=uWSGI daemon for ${SERVICE_NAME}
After=network.target

[Service]
ExecStart=${UWSGI_BIN} \
    --mount /=clic.web.index:app \
    --processes=2 \
    --chmod-socket=666 \
    -s ${UWSGI_SOCKET}
WorkingDirectory=${CLIC_PATH}
User=${UWSGI_USER}
Group=${UWSGI_GROUP}

[Install]
WantedBy=multi-user.target
EOF
[ -f "${UWSGI_SOCKET}" ] && chown ${UWSGI_USER}:${UWSGI_GROUP} "${UWSGI_SOCKET}"
systemctl enable ${SERVICE_NAME}.service
systemctl start ${SERVICE_NAME}.service

# ---------------------------

cat <<EOF > /etc/nginx/sites-available/${SERVICE_NAME}
upstream uwsgi_server {
    server unix://${UWSGI_SOCKET};
}

server {
    listen      80;
    server_name ${SERVER_NAME};
    charset     utf-8;

    proxy_intercept_errors on;
    location / {
        include uwsgi_params;
        # Emergency CLiC disabling rewrite rule, uncomment to disable clic access
        # rewrite ^(.*) /error/maintenance.html;
        uwsgi_pass  uwsgi_server;
        uwsgi_read_timeout ${UWSGI_TIMEOUT};

        error_page 502 503 504 /error/maintenance.html;
    }

    location /js {
        root ${CLIC_PATH}/clic/web/static;
        expires 1m;
    }
    location /css {
        root ${CLIC_PATH}/clic/web/static;
        expires 1m;
    }
    location /img {
        root ${CLIC_PATH}/clic/web/static;
        expires 1m;
    }
    location /fonts {
        root ${CLIC_PATH}/clic/web/static;
        expires 1m;
    }

    location /error {
        root ${CLIC_PATH}/clic/web/static/html;
    }
}
EOF
ln -fs /etc/nginx/sites-available/${SERVICE_NAME} /etc/nginx/sites-enabled/${SERVICE_NAME}
systemctl reload nginx.service
