from typing import Any, Annotated
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy.types import JSON


intpk = Annotated[int, mapped_column(primary_key=True)]
dtime = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('UTC', now())"))]

class Base(DeclarativeBase):
    type_annotation_map = {
        dict[str, Any]: JSON
    }


class SRActions(Base):
    __tablename__ = 'SRActions'

    id: Mapped[intpk]
    datetime: Mapped[dtime]
    master_activity: Mapped[str]
    activity_id: Mapped[str]
    task_id: Mapped[str]
    master_id: Mapped[str]
    assignment_id: Mapped[str] = mapped_column(nullable=True)
    status_id: Mapped[str] = mapped_column(nullable=True)
    comment_id: Mapped[str] = mapped_column(nullable=True)
    sd_id: Mapped[str] = mapped_column(nullable=True)


class SRTask(Base):
    __tablename__ = 'Tasks'

    id: Mapped[intpk]
    activity_id: Mapped[str]
    task_id: Mapped[str]
    project_id: Mapped[str]
    thematic_id: Mapped[str]
    master_id: Mapped[str]
    status: Mapped[str]
    data: Mapped[dict[str, Any]]


class SRStatus(Base):
    __tablename__ = 'Statuses'

    id: Mapped[intpk]
    activity_id: Mapped[str]
    status_id: Mapped[str]
    status: Mapped[str]


class SRAssignment(Base):
    __tablename__ = 'Assignments'

    id: Mapped[intpk]
    activity_id: Mapped[str]
    assignment_id: Mapped[str]
    assignee_master_id: Mapped[str]


class SD(Base):
    __tablename__ = 'SDs'

    id: Mapped[intpk]
    datetime: Mapped[dtime]
    activity_id: Mapped[str]
    sd_id: Mapped[str]
    master_id: Mapped[str]
    desc: Mapped[str]



class SRComment(Base):
    __tablename__ = 'Comments'

    id: Mapped[intpk]
    activity_id: Mapped[str]
    comment_id: Mapped[str]
    comment_text: Mapped[str]


class User(Base):
    __tablename__ = 'Users'

    id: Mapped[intpk]
    activity_id: Mapped[str]
    tg_id: Mapped[int]
    master_id: Mapped[str]
    user_status: Mapped[str]
    user_primary_group: Mapped[str]
    user_secondary_group: Mapped[str] = mapped_column(nullable=True)
#

class UserGroup(Base):
    __tablename__ = 'UserGroups'

    id: Mapped[intpk]
    activity_id: Mapped[str]
    group_id: Mapped[str]
    group_description: Mapped[str]
    users: Mapped[str]


class MasterActivity(Base):
    __tablename__ = 'MasterActivity'

    id: Mapped[intpk]
    datetime: Mapped[dtime]
    activity_id: Mapped[str]
    activity_slave_id: Mapped[str] = mapped_column(nullable=True)
    master_id: Mapped[str]
    interface: Mapped[str]