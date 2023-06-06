#!/usr/bin/env bash
flask db upgrade
flask create-user test 123456
gunicorn --worker-class eventlet -w 1 --bind=0.0.0.0:8080 admin:app

