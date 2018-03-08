import httplib

from flask import request, Response
from flask.views import MethodView

from auth.forms.facebook_connect_form import FacebookConnectForm


class FacebookConnectView(MethodView):
    def get(self):
        facebook_connect_form = FacebookConnectForm(request.args, csrf_enabled=False)

        if not facebook_connect_form.validate():
            return Response("Invalid form", status=httplib.BAD_REQUEST)

        account_info, created = facebook_connect_form.save_form()

        status = httplib.OK
        if created:
            status = httplib.CREATED

        return Response(str(account_info), status=status)
