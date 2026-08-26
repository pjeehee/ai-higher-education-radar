#!/bin/bash
cd "$(dirname "$0")"
python3 -m pip install -r requirements.txt
python3 backend/recompute_signals.py
python3 backend/app.py
