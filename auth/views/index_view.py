from flask import render_template, current_app, request
from flask.views import MethodView

from auth.helpers import get_facebook_redirect_uri


class IndexView(MethodView):
    def get(self):
        facebook_login_url = ("https://www.facebook.com/v2.12/dialog/oauth?"
                              "client_id={app_id}&redirect_uri={redirect_uri}")
        facebook_login_url = facebook_login_url.format(
            app_id=current_app.config['FACEBOOK_APP_ID'],
            redirect_uri=get_facebook_redirect_uri(),  # url root end with slash
        )

        context = {
            'facebook_login_url': facebook_login_url,
        }
        return render_template('auth/index.html', **context)
