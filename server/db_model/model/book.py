from datetime import datetime

from sqlalchemy import DateTime, UniqueConstraint

from server.db_instance import db


class BookModel(db.Model):
    __tablename__ = "book"

    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(32), nullable=False, unique=True)
    division = db.Column(db.String(32), nullable=False)
    file_path = db.Column(db.String(128), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    num_chapters = db.Column(db.Integer, nullable=False)
    insert_date = db.Column(DateTime(), nullable=False, default=datetime.utcnow)

    __table_args__ = (UniqueConstraint("title"),)

    @staticmethod
    def does_book_exist(title: str) -> bool:
        return db.session.query(BookModel.book_id).filter_by(title=title).scalar() is not None

    # todo: we might use these, and uncomment
    # chapters = db.relationship("Chapter", backref="book", lazy=True)
    # appearances = db.relationship("WordAppearance", backref="book", lazy=True)
