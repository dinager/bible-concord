from sqlalchemy import UniqueConstraint

from server.db_instance import db


class ChapterModel(db.Model):
    __tablename__ = "chapter"

    book_id = db.Column(db.Integer, db.ForeignKey("book.book_id", ondelete="CASCADE"), primary_key=True)
    num_chapter = db.Column(db.Integer, primary_key=True)
    num_verses = db.Column(db.Integer, nullable=False)

    __table_args__ = (UniqueConstraint("book_id", "num_chapter"),)

    @classmethod
    def get_num_verses(cls, book_id: int, chapter_number: int) -> int | None:
        # Query the chapter by book_id and chapter number
        chapter = (
            db.session.query(ChapterModel)
            .filter_by(book_id=book_id, num_chapter=chapter_number)
            .one_or_none()
        )
        if chapter is None:
            return -2

        return chapter.num_verses
