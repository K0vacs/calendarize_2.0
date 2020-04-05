#!/bin/bash

bool=true

while [ bool ]
do
    bool=false
    sleep 15
    python manage.py migrate
    python manage.py runserver 0.0.0.0:8000
done