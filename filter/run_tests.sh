#!/bin/bash

cd /home/tool/filter
virtualenv venv # creates a virtualenv in the ./venv directory
. venv/bin/activate
pip install -r requirements.txt
pip install nose -I
deactivate # need to refresh the virtualenv for correct `nose` to be used
. venv/bin/activate
nosetests
