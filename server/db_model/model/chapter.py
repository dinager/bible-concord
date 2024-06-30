from server.db_instance import db


class ChapterModel(db.Model):
    __tablename__ = "chapter"

    book_id = db.Column(db.Integer, db.ForeignKey("book.book_id", ondelete="CASCADE"), primary_key=True)
    num_chapter = db.Column(db.Integer, primary_key=True)
    num_verses = db.Column(db.Integer, nullable=False)
