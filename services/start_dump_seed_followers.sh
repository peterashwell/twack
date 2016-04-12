#!/bin/bash
source twackenv/bin/activate
source env.sh
source secrets.sh
python3 dump_seed_followers.py
