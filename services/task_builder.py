import asyncio

from services.activity_service import AlchemyMonster, ActivityService
from services.utils import ts, uuidg
from schemas.project_schema import projects
from models.data_models import *
from schemas.pydantic_schema import SRTaskAddSchema, SRActionWizardAddSchema, SDAddSchema


class Builder:

    def __GetStartAssigner(self, project, thematic):
        return projects['projects'][project]['issues_thematics'][thematic]['start_assigner']

    def __NewAssign(self, activity_id, assignee):
        data = SRAssignment(
            activity_id=activity_id,
            assignment_id=uuidg("AAN-"),
            assignee_master_id=assignee.upper(),
        )
        return data

    def __NewStatus(self, activity_id, NewStatus):
        data = SRStatus(
            activity_id=activity_id,
            status_id=uuidg("AST-"),
            status=NewStatus,
        )
        return data

    def __NewComment(self, activity_id, comment):
        data = SRComment(
            activity_id=activity_id,
            comment_id=uuidg("ACM-"),
            comment_text=comment,
        )
        return data

    def __NewActivity(self, task_id, master_activity, master_id, new_assign=None, new_status=None,
                      new_comment=None):
        activity_id = uuidg("AAC-")
        assignment_id, status_id, comment_id = None, None, None
        if new_assign is not None:
            new_assign = self.__NewAssign(activity_id, new_assign)
            assignment_id = new_assign.assignment_id
        if new_status is not None:
            new_status = self.__NewStatus(activity_id, new_status)
            status_id = new_status.status_id
        if new_comment is not None:
            new_comment = self.__NewComment(activity_id, new_comment)
            comment_id = new_comment.comment_id
        new_activity = SRActions(
            activity_id=activity_id,
            master_activity=master_activity,
            task_id=task_id,
            master_id=master_id,
            assignment_id=assignment_id,
            status_id=status_id,
            comment_id=comment_id,
        )
        return [new_activity, new_assign, new_status, new_comment]

    @classmethod
    async def SDBuilder(cls, sd: SDAddSchema):
        ...

    @classmethod
    async def TaskBuilder(cls, task: SRTaskAddSchema, master_activity):
        task_id = uuidg("XT-")
        new_assigner = task.assignee_master_id
        new_status = "NEW"
        if new_assigner is None:
            new_assigner = Builder().__GetStartAssigner(
                task.project_id,
                task.thematic_id)
        activity_models = Builder().__NewActivity(
            task_id=task_id,
            master_activity=master_activity,
            master_id=task.master_id,
            new_assign=new_assigner,
            new_status=new_status
        )
        print(activity_models)
        new_task = SRTask(
            activity_id=activity_models[0].activity_id,
            task_id=task_id,
            project_id=task.project_id,
            thematic_id=task.thematic_id,
            master_id=task.master_id.upper(),
            status=new_status,
            data=task.data,
        )

        return await Builder().__SendADDTaskTransaction((new_task, *activity_models), master_activity)

    @classmethod
    async def MultiActionWizard(cls, wizard: SRActionWizardAddSchema, master_activity: str):
        upd_models = Builder().__NewActivity(
            task_id=wizard.task_id,
            master_activity=master_activity,
            master_id=wizard.master_id,
            new_assign=wizard.assignee_master_id,
            new_status=wizard.status,
            new_comment=wizard.comment_text,
        )
        if wizard.status is not None:
            task_upd_model = SRTask(
                task_id=wizard.task_id,
                status=wizard.status,
            )
            upd_models.append(task_upd_model)
        master_activity = MasterActivity(
            activity_id=master_activity,
            activity_slave_id=upd_models[0].activity_id,
        )
        upd_models.append(master_activity)

        return await Builder().__MasterTransaction(upd_models)


    #
    @classmethod
    async def ActivityWizard(cls, wizard: SRActionWizardAddSchema):
        ...

    async def __SendADDTaskTransaction(self, mods, master_activity: str):
        stk = []
        for mod in mods:
            if mod is not None:
                stk.append(mod)
            task_res = await AlchemyMonster(models=stk).am_add()
        master_res = await ActivityService.UpdateMain(master_activity=master_activity,
                                                      slave_activity=mods[1].activity_id)
        print(f"{master_res=}\n{task_res=}")
        if master_res == task_res == True:
            return {"ok": True, "task_id": mods[0].task_id}

    async def __MasterTransaction(self, mods):
        stk = []
        for mod in mods:
            if mod is not None:
                stk.append(mod)
        rs = await AlchemyMonster(models=stk).upd_master()
        try:
            return {"ok": False, "detail": rs[1]}
        except Exception as e:
            print(e)
            return {"ok": True}
