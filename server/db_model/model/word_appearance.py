from sqlalchemy import UniqueConstraint

from server.db_instance import db


class WordAppearanceModel(db.Model):
    __tablename__ = "word_appearance"

    index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.book_id", ondelete="CASCADE"), nullable=False)
    word_id = db.Column(db.Integer, db.ForeignKey("word.word_id", ondelete="CASCADE"), nullable=False)
    verse_num = db.Column(db.Integer, nullable=False)
    chapter_num = db.Column(db.Integer, nullable=False)
    word_position = db.Column(db.Integer, nullable=False)

    __table_args__ = (UniqueConstraint("book_id", "word_id", "verse_num", "chapter_num", "word_position"),)

    # todo: we might use these, and uncomment
    # book = db.relationship("Book", backref="word_appearances")
    # word = db.relationship("Word", backref="word_appearances")
