from typing import Tuple

from sqlalchemy import UniqueConstraint
from sqlalchemy.exc import SQLAlchemyError

from server.db_instance import db


class GroupModel(db.Model):
    __tablename__ = "group"

    group_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    __table_args__ = (UniqueConstraint("name", name="uq_group_name"),)

    @classmethod
    def does_group_exist(cls, name: str) -> bool:
        return db.session.query(GroupModel.group_id).filter_by(name=name).scalar() is not None

    @classmethod
    def get_all_groups_names(cls) -> list[str]:
        return [row.name for row in db.session.query(GroupModel.name).all()]

    @classmethod
    def get_group_id(cls, group_name: str) -> int | None:
        return db.session.query(GroupModel.group_id).filter_by(name=group_name.lower()).scalar()

    @classmethod
    def insert_group(cls, group_name: str) -> None:
        session = db.session
        session.add(GroupModel(name=group_name))
        session.commit()

    @classmethod
    def delete_group_by_name(cls, group_name: str) -> Tuple[bool, str]:
        try:
            db.session.query(GroupModel).filter_by(name=group_name.lower()).delete()
            db.session.commit()
            return True, f"Group '{group_name}' deleted successfully."

        except SQLAlchemyError as e:
            db.session.rollback()  # Roll back the transaction
            return False, f"An error occurred: {str(e)}"
