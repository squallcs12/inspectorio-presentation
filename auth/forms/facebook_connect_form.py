import wtforms
from flask_wtf import FlaskForm
from wtforms import validators


class FacebookConnectForm(FlaskForm):
    code = wtforms.StringField(validators=[validators.DataRequired()])
