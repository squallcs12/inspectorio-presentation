from .blueprint import blueprint


class Auth(object):
    def init_app(self, app):
        self.init_blueprints(app)

    def init_blueprints(self, app):
        """

        :param app:
        :type app flask.Flask
        :return:
        """
        app.register_blueprint(blueprint)
