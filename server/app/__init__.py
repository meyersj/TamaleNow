# Copyright (C) 2015 Jeffrey Meyers
#
# This program is released under the "MIT License".
# Please see the file COPYING in this distribution for
# license terms.


from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app.mod_api.endpoints import mod_api as api_module

app.register_blueprint(api_module)



