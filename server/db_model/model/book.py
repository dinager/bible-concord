from datetime import datetime
from typing import Optional, Self, Tuple

from sqlalchemy import DateTime, UniqueConstraint
from sqlalchemy.exc import SQLAlchemyError

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

    # todo: we might use these, and uncomment
    # chapters = db.relationship("Chapter", backref="book", lazy=True)
    # appearances = db.relationship("WordAppearance", backref="book", lazy=True)

    @classmethod
    def does_book_exist(cls, title: str) -> bool:
        return db.session.query(BookModel.book_id).filter_by(title=title.lower()).scalar() is not None

    @classmethod
    def get_all_books(cls) -> list[Self]:
        return db.session.query(BookModel).all()

    @classmethod
    def get_all_book_names(cls) -> list[str]:
        return [row.title for row in db.session.query(BookModel.title).all()]

    @classmethod
    def get_book(cls, title: str) -> Self | None:
        return db.session.query(BookModel).filter_by(title=title.lower()).one_or_none()

    @classmethod
    def get_book_id(cls, title: str) -> int | None:
        return db.session.query(BookModel.book_id).filter_by(title=title.lower()).scalar()

    @classmethod
    def get_book_file_path(cls, title: str) -> str | None:
        return db.session.query(BookModel.file_path).filter_by(title=title.lower()).scalar()

    @classmethod
    def get_book_title_by_id(cls, book_id: int) -> Optional[str]:
        return db.session.query(cls.title).filter_by(book_id=book_id).scalar()

    @classmethod
    def delete_book_by_title(cls, title: str) -> Tuple[bool, str]:
        try:
            book_id = BookModel.get_book_id(title)
            db.session.delete(cls.query.get(book_id))
            db.session.commit()
            return True, f"Book '{title}' deleted successfully."

        except SQLAlchemyError as e:
            db.session.rollback()  # Roll back the transaction
            return False, f"An error occurred: {str(e)}"
