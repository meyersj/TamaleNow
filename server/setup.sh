#!/bin/bash

# Copyright (C) 2015 Jeffrey Meyers


rm -rf env
virtualenv env
./env/bin/pip install -r requirements.txt
