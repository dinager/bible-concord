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
    # group = db.relationship("Group", backref="word_in_group", lazy=True)

    __table_args__ = (UniqueConstraint("group_id", "word_id"),)

    @classmethod
    def get_words_in_group(cls, group_name: str) -> list[str]:
        group_id = GroupModel.get_group_id(group_name)
        words = (
            db.session.query(WordModel.value)
            .join(WordInGroupModel)
            .filter(WordInGroupModel.group_id == group_id)
            .order_by(WordModel.value)
            .all()
        )
        return [word.value for word in words]

    @classmethod
    def does_word_exist_in_group(cls, group_id: int, word_id: int) -> bool:
        return (
            db.session.query(WordInGroupModel.word_id)
            .filter_by(
                group_id=group_id,
                word_id=word_id,
            )
            .scalar()
            is not None
        )

    @classmethod
    def insert_word_to_group(cls, group_id: int, word_id: int) -> None:
        db.session.add(WordInGroupModel(group_id=group_id, word_id=word_id))
        db.session.commit()
        print("Data inserted successfully into word_in_group table.")
