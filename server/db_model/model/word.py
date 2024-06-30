# from typing import Self

from server.db_instance import db


class WordModel(db.Model):
    __tablename__ = "word"

    word_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String(50), nullable=False, unique=True)
    length = db.Column(db.Integer, nullable=False)

    __table_args__ = (db.Index("word_value_idx", "value", unique=True),)
