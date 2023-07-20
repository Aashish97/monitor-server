#!/bin/bash
source venv/bin/activate

pip install psutil requests

python monitor.py
