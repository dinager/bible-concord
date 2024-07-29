from typing import Tuple

from sqlalchemy import UniqueConstraint
from sqlalchemy.exc import SQLAlchemyError

from server.db_instance import db


class PhraseModel(db.Model):
    __tablename__ = "phrase"

    phrase_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    __table_args__ = (UniqueConstraint("name", name="uq_group_name"),)

    @classmethod
    def does_phrase_exist(cls, name: str) -> bool:
        return db.session.query(PhraseModel.phrase_id).filter_by(name=name).scalar() is not None

    @classmethod
    def get_all_phrases_names(cls) -> list[str]:
        return [row.name for row in db.session.query(PhraseModel.name).all()]

    @classmethod
    def get_phrase_id(cls, phrase_name: str) -> int | None:
        return db.session.query(PhraseModel.phrase_id).filter_by(name=phrase_name.lower()).scalar()

    @classmethod
    def insert_phrase_to_phrase_table(cls, phrase_name: str) -> None:
        session = db.session
        session.add(PhraseModel(name=phrase_name))
        session.commit()

    @classmethod
    def delete_phrase_from_phrase_table(cls, phrase_name: str) -> None:
        session = db.session
        phrase = session.query(PhraseModel).filter_by(name=phrase_name).first()
        if phrase:
            session.delete(phrase)
            session.commit()
        else:
            raise ValueError(f"Phrase '{phrase_name}' not found in the database.")

    @classmethod
    def delete_phrase_by_name(cls, phrase_name: str) -> Tuple[bool, str]:
        try:
            phrase_id = PhraseModel.get_phrase_id(phrase_name)
            db.session.delete(cls.query.get(phrase_id))
            db.session.commit()
            return True, f"phrase '{phrase_name}' deleted successfully."

        except SQLAlchemyError as e:
            db.session.rollback()  # Roll back the transaction
            return False, f"An error occurred: {str(e)}"
