from flask import Blueprint

from auth.views import IndexView, FacebookConnectView

blueprint = Blueprint('auth', __name__, url_prefix='/auth')

blueprint.add_url_rule('/', 'index', IndexView.as_view(__name__))
blueprint.add_url_rule('/connect_with_facebook', 'connect_with_facebook', FacebookConnectView.as_view(__name__))
