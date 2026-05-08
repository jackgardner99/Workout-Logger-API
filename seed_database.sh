#!/bin/bash

python manage.py migrate
python manage.py loaddata users tokens intensity muscle_groups categories exercises
