import httplib

import facebook
from flask import current_app, request, Response
from flask.views import MethodView

from auth.forms.facebook_connect_form import FacebookConnectForm
from auth.helpers import get_facebook_redirect_uri
from auth.models import User


class FacebookConnectView(MethodView):
    def get(self):
        facebook_connect_form = FacebookConnectForm(request.args, csrf_enabled=False)

        if not facebook_connect_form.validate():
            return Response("Invalid form", status=httplib.BAD_REQUEST)
        code = facebook_connect_form.code.data

        access_token = facebook.GraphAPI().get_access_token_from_code(
            code, get_facebook_redirect_uri(), current_app.config['FACEBOOK_APP_ID'],
            current_app.config['FACEBOOK_APP_SECRET']
        )

        access_token = access_token['access_token']

        facebook_api = facebook.GraphAPI(access_token)
        account_info = facebook_api.get_object('me')

        user = User(facebook_id=account_info['id'], name=account_info['name'])
        current_app.db.session.add(user)
        current_app.db.session.commit()

        return Response(str(account_info))
