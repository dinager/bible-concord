# from typing import Self

from typing import List

from server.db_instance import db


class WordModel(db.Model):
    __tablename__ = "word"

    word_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String(50), nullable=False, unique=True)
    length = db.Column(db.Integer, nullable=False)

    __table_args__ = (db.Index("word_value_idx", "value", unique=True),)

    @staticmethod
    def get_existing_words(words: list[str]) -> list["WordModel"]:
        if not words:
            return []
        query = db.session.query(WordModel).filter(WordModel.value.in_(words))
        return query.all()

    @staticmethod
    # Function to get word_ids that start with a given prefix
    def get_word_ids_starting_with(prefix: str) -> List[str]:
        # Query the database to get word_ids that start with the given prefix
        words = db.session.query(WordModel).filter(WordModel.value.startswith(prefix)).all()
        # Return a list of word_ids for the words that match the prefix
        return [word.word_id for word in words]
