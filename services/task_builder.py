from uuid import uuid4
from datetime import datetime as dt
from schemas.project_schema import projects
from models.data_models import *
from schemas.pydantic_schema import SRTaskAddSchema, SRActionWizardAddSchema
from db.db import new_session


def ts():
    a = dt.now().strftime("%Y-%m-%d %H:%M:%S")
    return a


class Validation:
    status: bool
    details: str
    status_code: int = 200

    @classmethod
    def set_validation(cls, status=True, details="success"):
        Validation.details = details
        Validation.status = status
        if not status:
            Validation.status_code = 422


v = Validation()
setv = v.set_validation


class Builder:

    @classmethod
    def uuid_generator(cls, prefix=None):
        uuid_short = str(uuid4())[-8:]
        if prefix is not None:
            uuid_short = prefix + uuid_short
        # uuid_long = str(uuid4())
        return uuid_short.upper()

    def __GetStartAssigner(self, project, thematic):
        return projects['projects'][project]['issues_thematics'][thematic]['start_assigner']

    def __NewAssign(self, dtime, activity_id, assignee):
        data = SRAssignment(
            datetime=dtime,
            activity_id=activity_id,
            assignment_id=self.uuid_generator("AAN-"),
            assignee_master_id=assignee.upper(),
        )
        return data

    def __NewStatus(self, dtime, activity_id, NewStatus):
        data = SRStatus(
            datetime=dtime,
            activity_id=activity_id,
            status_id=self.uuid_generator("AST-"),
            status=NewStatus,
        )
        return data

    def __NewComment(self, dtime, activity_id, comment):
        data = SRComment(
            datetime=dtime,
            activity_id=activity_id,
            comment_id=self.uuid_generator("ACM-"),
            comment_text=comment,
        )
        return data

    def __NewActivity(self, dtime, task_id, master_id, new_assign=None, new_status=None, new_comment=None):
        activity_id = self.uuid_generator("AAC-")
        assignment_id, status_id, comment_id = None, None, None
        if new_assign is not None:
            new_assign = self.__NewAssign(dtime, activity_id, new_assign)
            assignment_id = new_assign.assignment_id
        if new_status is not None:
            new_status = self.__NewStatus(dtime, activity_id, new_status)
            status_id = new_status.status_id
        if new_comment is not None:
            new_comment = self.__NewComment(dtime, activity_id, new_comment)
            comment_id = new_comment.comment_id
        new_activity = SRActions(
            datetime=dtime,
            activity_id=activity_id,
            task_id=task_id,
            master_id=master_id,
            assignment_id=assignment_id,
            status_id=status_id,
            comment_id=comment_id,
        )
        return new_activity, new_assign, new_status, new_comment

    @classmethod
    async def TaskBuilder(cls, task: SRTaskAddSchema):
        dtime = ts()
        task_id = Builder.uuid_generator("XT-")
        new_assigner = task.assignee_master_id
        new_status = "NEW"
        if new_assigner is None:
            new_assigner = Builder().__GetStartAssigner(
                task.project_id,
                task.thematic_id)
        activity_models = Builder().__NewActivity(
            dtime=dtime,
            task_id=task_id,
            master_id=task.master_id,
            new_assign=new_assigner,
            new_status=new_status
        )
        new_task = SRTask(
            datetime=dtime,
            activity_id=activity_models[0].activity_id,
            task_id=task_id,
            project_id=task.project_id,
            thematic_id=task.thematic_id,
            master_id=task.master_id.upper(),
            status=new_status,
            data=task.data,
        )
        await Builder().__SendTransaction(new_task, *activity_models)
        return v

    @classmethod
    async def ActionWizard(cls, wizard: SRActionWizardAddSchema):
        dtime = ts()
        activity_models = Builder().__NewActivity(
            dtime=dtime,
            task_id=wizard.task_id,
            master_id=wizard.master_id,
            new_assign=wizard.new_assign,
            new_status=wizard.new_status,
            new_comment=wizard.new_comment,
        )

    async def __SendTransaction(self, new_task, new_activity, new_assign, new_status, new_comment):
        async with new_session() as session:
            if new_task is not None:
                session.add(new_task)
            if new_activity is not None:
                session.add(new_activity)
            if new_assign is not None:
                session.add(new_assign)
            if new_status is not None:
                session.add(new_status)
            if new_comment is not None:
                session.add(new_comment)
            try:
                await session.commit()
                setv(status=True, details={"task": "ok", "task_id": new_task.task_id})
            except:
                await session.rollback()
