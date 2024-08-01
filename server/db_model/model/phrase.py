from sqlalchemy import UniqueConstraint

from server.db_instance import db


class PhraseModel(db.Model):
    __tablename__ = "phrase"

    phrase_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phrase_text = db.Column(db.String(100), nullable=False, unique=True)

    __table_args__ = (UniqueConstraint("phrase_text", name="uq_group_name"),)

    @classmethod
    def does_phrase_exist(cls, phrase_text: str) -> bool:
        return db.session.query(PhraseModel.phrase_id).filter_by(phrase_text=phrase_text).scalar() is not None

    @classmethod
    def get_all_phrases_names(cls) -> list[str]:
        return [row.phrase_text for row in db.session.query(PhraseModel.phrase_text).all()]

    @classmethod
    def insert_phrase(cls, phrase_text: str) -> None:
        session = db.session
        session.add(PhraseModel(phrase_text=phrase_text))
        session.commit()

    @classmethod
    def delete_phrase_by_name(cls, phrase_text: str) -> None:
        db.session.query(PhraseModel).filter_by(phrase_text=phrase_text.lower()).delete()
        db.session.commit()
