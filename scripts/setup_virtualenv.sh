#!/bin/bash

cd /home/ubuntu/soWolfkrieg/wolfskrieg
python3 -m pip install virtualenv
virtualenv venv
source ./venv/bin/activate
pip install flask
pip install requests
pip install eml_parser
export FLASK_APP=/home/ubuntu/soWolfkrieg/wolfskrieg/app.py
