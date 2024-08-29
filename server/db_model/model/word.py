from typing import Self

from server.db_instance import db


class WordModel(db.Model):
    __tablename__ = "word"

    word_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String(50), nullable=False, unique=True)
    length = db.Column(db.Integer, nullable=False)

    @classmethod
    def get_existing_words(cls, words: list[str]) -> list[Self]:
        if not words:
            return []
        query = db.session.query(WordModel).filter(WordModel.value.in_(words))
        return query.all()

    @classmethod
    def get_word_id(cls, value: str) -> int:
        return db.session.query(WordModel.word_id).filter_by(value=value.lower()).scalar()
