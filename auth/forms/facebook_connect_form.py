import facebook
import wtforms
from flask import current_app
from flask_wtf import FlaskForm
from wtforms import validators

from auth.helpers import get_facebook_redirect_uri
from auth.models import User


class FacebookConnectForm(FlaskForm):
    code = wtforms.StringField(validators=[validators.DataRequired()])

    def save_form(self):
        code = self.code.data

        access_token = facebook.GraphAPI().get_access_token_from_code(
            code, get_facebook_redirect_uri(), current_app.config['FACEBOOK_APP_ID'],
            current_app.config['FACEBOOK_APP_SECRET']
        )

        access_token = access_token['access_token']

        facebook_api = facebook.GraphAPI(access_token)
        account_info = facebook_api.get_object('me')

        user = User.query.filter_by(facebook_id=account_info['id']).first()
        created = False
        if not user:
            user = User(facebook_id=account_info['id'], name=account_info['name'])
            current_app.db.session.add(user)
            current_app.db.session.commit()
            created = True

        return account_info, created

