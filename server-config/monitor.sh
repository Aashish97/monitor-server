#!/bin/bash
source venv/bin/activate

while true; do
    python monitor.py;
    sleep 10;
done
