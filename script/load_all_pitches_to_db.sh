#!/bin/sh
find ../data/pitches -name *.xml | xargs -L 1 ./load_pitches_to_db.py