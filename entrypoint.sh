#!/usr/bin/env bash
flask db upgrade
gunicorn --worker-class eventlet -w 1 --bind=0.0.0.0:8080 admin:app

