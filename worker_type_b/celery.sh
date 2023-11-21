#!/usr/bin/env bash

WORKER_TYPE='type-b'
CELERY_SCALE=10

mkdir -p /var/run/celery /var/log/celery
chown -R nobody:nogroup /var/run/celery /var/log/celery

exec celery --app=worker worker \
            --autoscale ${CELERY_SCALE} \
            --loglevel=INFO \
            --hostname=worker-${WORKER_TYPE}@%h \
            --queues=${WORKER_TYPE} \
            --uid=nobody --gid=nogroup

#            --logfile=/var/log/celery/worker.log \
#            --statedb=/var/run/celery/worker@%h.state \
