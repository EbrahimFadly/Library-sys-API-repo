from . import db


class reader(db.Model):
    __tablename__ = "reader"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    books = db.relationship("book", backref="reader", lazy=True)


class librarian(db.Model):
    __tablename__ = "librarian"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
