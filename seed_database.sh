#!/bin/bash

python manage.py migrate
python manage.py loaddata users tokens intensity muscle_groups categories exercises muscle_exercises workout_logs log_exercises
