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

# in a real app, these should be configured through Flask-Appconfig
# app.config['SECRET_KEY'] = 'devkey'
# app.config['RECAPTCHA_PUBLIC_KEY'] = \
#     '6Lfol9cSAAAAADAkodaYl9wvQCwBMr3qGR_PPHcw'

class SentimentForm(Form):
    sentence = TextField('Type your sentence here', validators=[Required()])
    radio_field = RadioField('This is a radio field', choices=[
        ('bernb', 'BernoulliNB'),
        ('multi', 'Multinomial'),
        ('logreg', 'Logistic Regression'),
        ('svc', 'SVC'),
        ('lsvc', 'LinearSVC'),
    ])

    submit_button = SubmitField('Submit')

@app.route('/', methods=('GET', 'POST'))
def index():
    # form = ExampleForm()
    form = SentimentForm()
    form.validate_on_submit()  # to get error messages to the browser
    # flash('critical message', 'critical')
    # flash('error message', 'error')
    # flash('warning message', 'warning')
    # flash('info message', 'info')
    # flash('debug message', 'debug')
    # flash('different message', 'different')
    # flash('uncategorized message')

    if form.validate_on_submit():
        if request.method == 'POST':
            result = request.form
            print(result)

            return render_template('result.html', form=form)
        
        else:
            print('ELSEEEE')
            print(request.form)
            # print(form.csrf_token)
            return render_template('error.html', form=form)     

        return render_template('index.html', form=form)

    return app

if __name__ == '__main__':
    create_app().run(debug=True)
