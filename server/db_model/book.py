from datetime import datetime

from sqlalchemy import DateTime

from server.db_instance import db


class Book(db.Model):
    __tablename__ = "book"

    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(32), nullable=False, unique=True)
    division = db.Column(db.String(32), nullable=False)
    file_path = db.Column(db.String(128), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    num_chapters = db.Column(db.Integer, nullable=False)
    insert_date = db.Column(DateTime(), nullable=False, default=datetime.utcnow)

    # todo: we might use these, and uncomment
    # chapters = db.relationship("Chapter", backref="book", lazy=True)
    # appearances = db.relationship("WordAppearance", backref="book", lazy=True)
