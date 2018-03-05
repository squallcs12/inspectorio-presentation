from flask import request


def get_facebook_redirect_uri():
    return '{}auth/connect_with_facebook'.format(request.url_root)
