import asyncio

from services.activity_service import AlchemyMonster, ActivityService
from services.utils import ts, uuidg
from schemas.project_schema import projects
from models.data_models import *
from schemas.pydantic_schema import SRTaskAddSchema, SRActionWizardAddSchema, SDAddSchema


class Builder:

    def __GetStartAssigner(self, project, thematic):
        return projects['projects'][project]['issues_thematics'][thematic]['start_assigner']

    def __NewAssign(self, dtime, activity_id, assignee):
        data = SRAssignment(
            datetime=dtime,
            activity_id=activity_id,
            assignment_id=uuidg("AAN-"),
            assignee_master_id=assignee.upper(),
        )
        return data

    def __NewStatus(self, dtime, activity_id, NewStatus):
        data = SRStatus(
            datetime=dtime,
            activity_id=activity_id,
            status_id=uuidg("AST-"),
            status=NewStatus,
        )
        return data

    def __NewComment(self, dtime, activity_id, comment):
        data = SRComment(
            datetime=dtime,
            activity_id=activity_id,
            comment_id=uuidg("ACM-"),
            comment_text=comment,
        )
        return data

    def __NewActivity(self, dtime, task_id, master_activity, master_id, new_assign=None, new_status=None,
                      new_comment=None):
        activity_id = uuidg("AAC-")
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
            master_activity=master_activity,
            task_id=task_id,
            master_id=master_id,
            assignment_id=assignment_id,
            status_id=status_id,
            comment_id=comment_id,
        )
        return new_activity, new_assign, new_status, new_comment

    @classmethod
    async def SDBuilder(cls, sd: SDAddSchema):
        ...

    @classmethod
    async def TaskBuilder(cls, task: SRTaskAddSchema, master_activity):
        dtime = ts()
        task_id = uuidg("XT-")
        new_assigner = task.assignee_master_id
        new_status = "NEW"
        if new_assigner is None:
            new_assigner = Builder().__GetStartAssigner(
                task.project_id,
                task.thematic_id)
        activity_models = Builder().__NewActivity(
            dtime=dtime,
            task_id=task_id,
            master_activity=master_activity,
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

        return await Builder().__SendTransaction((new_task, *activity_models), master_activity)

    @classmethod
    async def ActionWizard(cls, wizard: SRActionWizardAddSchema):
        dtime = ts()
        activity_models = Builder().__NewActivity(
            dtime=dtime,
            task_id=wizard.task_id,
            master_id=wizard.master_id,
            new_assign=wizard.assignee_master_id,
            new_status=wizard.status,
            new_comment=wizard.comment_text,

        )

    #
    @classmethod
    async def ActivityWizard(cls, wizard: SRActionWizardAddSchema):
        ...

    async def __SendTransaction(self, mods, master_activity: str):
        stk = []
        for mod in mods:
            if mod is not None:
                stk.append(mod)
            task_res = await AlchemyMonster(models=stk).am_add()
        master_res = await ActivityService.UpdateMain(master_activity=master_activity,
                                                      slave_activity=mods[2].activity_id)
        print(f"{master_res=}\n{task_res=}")
        if master_res == task_res == True:
            return {"ok": True, "task_id": mods[0].task_id}
