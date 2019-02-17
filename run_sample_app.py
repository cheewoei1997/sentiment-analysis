# under normal circumstances, this script would not be necessary. the
# sample_application would have its own setup.py and be properly installed;
# however since it is not bundled in the sdist package, we need some hacks
# to make it work

import os
import sys
from flask import Flask, render_template, flash, request
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig
from flask_wtf import Form, RecaptchaField
from flask_wtf.file import FileField
from wtforms import TextField, HiddenField, ValidationError, RadioField,\
    BooleanField, SubmitField, IntegerField, FormField, validators
from wtforms.validators import Required
# from analyser import set_data

sys.path.append(os.path.dirname(__name__))

from sample_application import create_app

# create an app instance
# app = create_app()

# app.run(debug=True)

app = Flask(__name__)
AppConfig(app, None)  # Flask-Appconfig is not necessary, but
                            # highly recommend =)
                            # https://github.com/mbr/flask-appconfig
Bootstrap(app)


if __name__ == '__main__':
    create_app().run(debug=True)
