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

# ---------------------------

systemctl | grep -q "${SERVICE_NAME}.service" && systemctl stop ${SERVICE_NAME}.service
cat <<EOF > ${SERVICE_FILE}
[Unit]
Description=uWSGI daemon for ${SERVICE_NAME}
After=network.target

[Service]
ExecStart=${UWSGI_BIN} \
    --mount /=clic.web.index:app \
    --processes=5 \
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

# Hardcoded uwsgi_params.
uwsgi_param  QUERY_STRING       \$query_string;
uwsgi_param  REQUEST_METHOD     \$request_method;
uwsgi_param  CONTENT_TYPE       \$content_type;
uwsgi_param  CONTENT_LENGTH     \$content_length;
uwsgi_param  REQUEST_URI        \$request_uri;
uwsgi_param  PATH_INFO          \$document_uri;
uwsgi_param  DOCUMENT_ROOT      \$document_root;
uwsgi_param  SERVER_PROTOCOL    \$server_protocol;
uwsgi_param  HTTPS              \$https if_not_empty;
uwsgi_param  REMOTE_ADDR        \$remote_addr;
uwsgi_param  REMOTE_PORT        \$remote_port;
uwsgi_param  SERVER_PORT        \$server_port;
uwsgi_param  SERVER_NAME        \$server_name;

server {
    listen      80;
    server_name ${SERVER_NAME};
    charset     utf-8;

    location / {
        uwsgi_pass  uwsgi_server;
    }
}
EOF
ln -fs /etc/nginx/sites-available/${SERVICE_NAME} /etc/nginx/sites-enabled/${SERVICE_NAME}
systemctl reload nginx.service
