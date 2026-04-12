#!/bin/bash

# Start cron daemon
service cron start

# Run the app
python app.py
