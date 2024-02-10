#!/usr/bin/env bash
set -e

WORKERS_COUNT="${WORKERS_COUNT:-4}"
THREADS_COUNT="${THREADS_COUNT:-8}"
WORKERS_CONCURRENCY="${WORKERS_CONCURRENCY:-4}"

execute_db_migration() {
  # Apply migrations
  echo 'Migrating DB...'
  python manage.py migrate || {
    echo "!!! DB migrations failed but ignoring it... !!!"
  }
  echo
}

collect_static_files() {
  echo 'Collecting static files...'
  python manage.py collectstatic --no-input || {
    echo "!!! Collecting static files failed but ignoring it... !!!"
  }
  echo
}

start_api_server() {
  echo "=============== Starting API server ==============="
  gunicorn --bind 0.0.0.0:8000 job_journey.asgi:application -w "${WORKERS_COUNT}" --threads "${THREADS_COUNT}" -k uvicorn.workers.UvicornWorker --error-logfile - --access-logfile - --capture-output
}

BEAT_SCHEDULE_FILE=${BEAT_SCHEDULE_FILE:='./.beat_schedule'}
CELERY_BROKER_URL=${CELERY_BROKER_URL:-${REDIS_URL}}
CONTAINER_TYPE=${CONTAINER_TYPE:='api_server'}

case ${CONTAINER_TYPE} in
  api_server)
    execute_db_migration
    collect_static_files
    start_api_server
    ;;
  celery_beat)
    celery -A job_journey beat -s "${BEAT_SCHEDULE_FILE}" --loglevel=INFO
    ;;
  celery_worker_default)
    celery -A job_journey worker --loglevel=INFO -E -c "${WORKERS_CONCURRENCY}" -n "${CONTAINER_TYPE}"@%h
    ;;
  celery_flower)
    celery --result-backend "${CELERY_RESULT_BACKEND}" -b "${CELERY_BROKER_URL}" -A job_journey flower  --purge_offline_workers=300 --persistent=True --natural_time=True --broker_api="${CELERY_FLOWER_BROKER_API}" --loglevel=INFO
    ;;
  *)
    echo "CONTAINER_TYPE has to be defined!"
    exit 1
esac
