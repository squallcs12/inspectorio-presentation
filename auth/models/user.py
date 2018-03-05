from database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    facebook_id = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __str__(self):
        return self.name
