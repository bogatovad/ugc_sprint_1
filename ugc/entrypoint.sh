#!/bin/sh

wait_for_service() {
  local name="$1" host="$2" port="$3" retry_interval="$4"
  echo "Waiting for $name..."
  while ! nc -z $host $port; do
    sleep $retry_interval
  done
  echo "$name started"
}

wait_for_service "Kafka_UGC" $KAFKA_HOST $KAFKA_PORT 0.5


exec "$@"