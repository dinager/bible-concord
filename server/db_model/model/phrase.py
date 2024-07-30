from typing import Tuple

from sqlalchemy import UniqueConstraint
from sqlalchemy.exc import SQLAlchemyError

from server.db_instance import db
from server.db_model.model.phrase_reference import PhraseReference


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
    def insert_phrase_to_tables(cls, phrase_name: str, phrase_references: list[PhraseReference]) -> None:
        from server.db_model.model.phrase_reference import PhraseReferenceModel

        session = db.session

        try:
            # Create new phrase
            new_phrase = PhraseModel(name=phrase_name)
            session.add(new_phrase)
            session.flush()  # Ensures new_phrase.phrase_id is available

            # Create new phrase references
            phrase_id = new_phrase.phrase_id
            phrase_references_models = [
                PhraseReferenceModel(
                    phrase_id=phrase_id,
                    book_id=reference["book_id"],
                    chapter_num=reference["chapter_num"],
                    verse_num=reference["verse_num"],
                    word_position=reference["word_position"],
                    line_num_in_file=reference["line_num_in_file"],
                )
                for reference in phrase_references
            ]
            session.add_all(phrase_references_models)
            session.commit()

        except Exception as e:
            session.rollback()  # Rollback the transaction on error
            print(f"An error occurred: {e}")
            raise e
        finally:
            session.close

    @classmethod
    def delete_phrase_by_name(cls, phrase_name: str) -> Tuple[bool, str]:
        try:
            db.session.query(PhraseModel).filter_by(name=phrase_name.lower()).delete()
            db.session.commit()
            return True, f"phrase {phrase_name} deleted successfully"

        except SQLAlchemyError as e:
            db.session.rollback()
            return False, str(e)
