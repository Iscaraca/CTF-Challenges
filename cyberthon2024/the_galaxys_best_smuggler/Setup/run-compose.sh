#!/bin/sh

dockerd &
sleep 5

export PROXY_PORT=$2
export PLAYER_PORT=$3

docker compose -p $1 up -d --build

sleep 300

docker compose -p $1 down --volumes