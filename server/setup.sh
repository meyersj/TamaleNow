#!/bin/bash

# Copyright (C) 2015 Jeffrey Meyers
#
# This program is released under the "MIT License".
# Please see the file COPYING in this distribution for
# license terms.


rm -rf env
virtualenv env
./env/bin/pip install -r requirements.txt
