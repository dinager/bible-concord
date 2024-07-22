from sqlalchemy import UniqueConstraint

from server.db_instance import db
from server.db_model.model.group import GroupModel
from server.db_model.model.word import WordModel


class WordInGroupModel(db.Model):
    __tablename__ = "word_in_group"

    group_id = db.Column(
        db.Integer, db.ForeignKey("group.group_id", ondelete="CASCADE"), primary_key=True, nullable=False
    )
    word_id = db.Column(
        db.Integer, db.ForeignKey("word.word_id", ondelete="CASCADE"), primary_key=True, nullable=False
    )

    __table_args__ = (UniqueConstraint("group_id", "word_id"),)

    @staticmethod
    def get_words_in_group_from_db(group_name: str) -> list[str]:
        group_id = WordInGroupModel.get_group_id_by_name(group_name.lower())
        words = (
            db.session.query(WordModel.value)
            .join(WordInGroupModel)
            .filter(WordInGroupModel.group_id == group_id)
            .all()
        )
        return [word.value for word in words]

    @staticmethod
    def get_group_id_by_name(group_name: str) -> int:
        group_id = db.session.query(GroupModel.group_id).filter_by(name=group_name).first()
        return group_id[0] if group_id else None
