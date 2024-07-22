from typing import List

from sqlalchemy import UniqueConstraint

from server.db_instance import db


class GroupModel(db.Model):
    __tablename__ = "group"

    group_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    __table_args__ = (UniqueConstraint("name", name="uq_group_name"),)

    @staticmethod
    def does_group_exist(name: str) -> bool:
        return db.session.query(GroupModel.group_id).filter_by(name=name).scalar() is not None

    @staticmethod
    def get_all_groups() -> List["GroupModel"]:
        return db.session.query(GroupModel).all()
