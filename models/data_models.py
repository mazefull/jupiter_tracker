from typing import Any

from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy.types import JSON


class Base(DeclarativeBase):
    type_annotation_map = {
        dict[str, Any]: JSON
    }


class SRActions(Base):
    __tablename__ = 'SRActions'

    id: Mapped[int] = mapped_column(primary_key=True)
    datetime: Mapped[str]
    activity_id: Mapped[str]
    task_id: Mapped[str]
    master_id: Mapped[str]
    assignment_id: Mapped[str] = mapped_column(nullable=True)
    status_id: Mapped[str] = mapped_column(nullable=True)
    comment_id: Mapped[str] = mapped_column(nullable=True)


class SRTask(Base):
    __tablename__ = 'Tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    datetime: Mapped[str]
    activity_id: Mapped[str]
    task_id: Mapped[str]
    project_id: Mapped[str]
    thematic_id: Mapped[str]
    master_id: Mapped[str]
    status: Mapped[str]
    data: Mapped[dict[str, Any]]


class SRStatus(Base):
    __tablename__ = 'Statuses'

    id: Mapped[int] = mapped_column(primary_key=True)
    datetime: Mapped[str]
    activity_id: Mapped[str]
    status_id: Mapped[str]
    status: Mapped[str]


class SRAssignment(Base):
    __tablename__ = 'Assignments'

    id: Mapped[int] = mapped_column(primary_key=True)
    datetime: Mapped[str]
    activity_id: Mapped[str]
    assignment_id: Mapped[str]
    assignee_master_id: Mapped[str]


class SRComment(Base):
    __tablename__ = 'Comments'

    id: Mapped[int] = mapped_column(primary_key=True)
    datetime: Mapped[str]
    activity_id: Mapped[str]
    comment_id: Mapped[str]
    comment_text: Mapped[str]


class User(Base):
    __tablename__ = 'Users'

    id: Mapped[int] = mapped_column(primary_key=True)
    datetime: Mapped[str]
    tg_id: Mapped[int]
    master_id: Mapped[str]
    user_status: Mapped[str]
    user_primary_group: Mapped[str]
    user_secondary_group: Mapped[str] = mapped_column(nullable=True)


class UserGroup(Base):
    __tablename__ = 'UserGroups'

    id: Mapped[int] = mapped_column(primary_key=True)
    datetime: Mapped[str]
    group_id: Mapped[str]
    group_description: Mapped[str]
    users: Mapped[str]
