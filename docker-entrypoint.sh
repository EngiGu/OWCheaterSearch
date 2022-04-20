#!/bin/sh

cd  /app
gunicorn app:app --bind 0.0.0.0:9901 --worker-class sanic.worker.GunicornWorker -w 3

