#!/usr/bin/env bash
flask db upgrade
waitress-serve admin:app

