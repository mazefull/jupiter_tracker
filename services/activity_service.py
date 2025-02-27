from sqlalchemy import update, select, text
from services.utils import ts, uuidg
from models.data_models import MasterActivity, SRTask
from db.db import new_session


class ActivityService:
    @classmethod
    async def MainWizard(cls, master_id: str, interface: str):
        mdata = MasterActivity(
            activity_id=uuidg("MGA-"),
            activity_slave_id=None,
            master_id=master_id,
            interface=interface,
        )
        if await AlchemyMonster(models=(mdata,)).am_add():
            return mdata.activity_id

    #
    @classmethod
    async def UpdateMain(cls, master_activity, slave_activity):
        mdata = MasterActivity(
            activity_id=master_activity,
            activity_slave_id=slave_activity,
        )
        return await AlchemyMonster(models=mdata).insert_slave_activity()


class Validators:
    @classmethod
    async def IsTaskExsist(cls, task_id):
        mdata = SRTask(task_id=task_id)
        return await AlchemyMonster(models=mdata).is_task_exist()

    @classmethod
    async def GetTaskData(cls, task_id):
        mdata = SRTask(task_id=task_id)
        return await AlchemyMonster(models=mdata).get_task_data()
        """
        :param task_id:
        :return:
        """
        ...


class AlchemyMonster:
    def __init__(self, models):
        self.mods = models

    async def am_add(self):
        async with new_session() as session:
            for mod in self.mods:
                session.add(mod)
            try:
                await session.commit()
                return True
            except Exception as e:
                await session.rollback()
                print(f"DB Error: {e}")
                return False, e

    async def insert_slave_activity(self):
        async with (new_session() as session):
            qr = select(self.mods.__class__.id).where(
                self.mods.__table__.c.activity_id == self.mods.activity_id
            )
            tt = await session.execute(qr)
            if tt.scalar_one() is not None:
                stmt = update(self.mods.__class__).values(
                    activity_slave_id=self.mods.activity_slave_id
                ).where(
                    self.mods.__table__.c.activity_id == self.mods.activity_id
                )
                await session.execute(stmt)
                await session.commit()
                return True
            return False

    async def upd_master(self):
        async with new_session() as session:
            for mod in self.mods:
                if mod.__tablename__ == SRTask.__tablename__:
                    print('YES')
                    stmt = (
                        update(mod.__class__)
                        .values(status=mod.status)
                        .where(mod.__table__.c.task_id == mod.task_id)
                    )
                    await session.execute(stmt)
                elif mod.__tablename__ == MasterActivity.__tablename__:
                    stmt = (
                        update(mod.__class__)
                        .values(activity_slave_id=mod.activity_slave_id)
                        .where(mod.__table__.c.activity_id == mod.activity_id)
                    )
                    await session.execute(stmt)
                else:
                    session.add(mod)
            try:
                await session.commit()
                return True
            except Exception as e:
                session.rollback()
                print(f"DB Error: {e}")
                return False, e

    async def is_task_exist(self):
            async with new_session() as session:
                qr = (
                    select(self.mods.__class__.id)
                    .where(self.mods.__table__.c.task_id == self.mods.task_id)
                )
                tt = await session.execute(qr)
                try:
                    if tt.scalar_one() is not None:
                        return True
                except Exception as e:
                    return False

    async def get_task_data(self):
        async with new_session() as session:
            res_tasks = await session.execute(text("SELECT * FROM public.\"Tasks\" WHERE task_id = :task;", task=self.mods.task_id))
            res_actions = await session.execute(
                text("SELECT datetime, master_activity, activity_id, master_id, assignment_id, status_id, comment_id "
                     "FROM public.\"SRActions\" WHERE task_id = :task ORDER BY id DESC;", task=self.mods.task_id))
            return await DataPreparation.TaskDataLoader(res_tasks.all(), res_actions.all())

    @classmethod
    async def get_task_comments_data(cls, ids):
        async with new_session() as session:
            comment_dt = []
            for _id in ids:
                res_comm = await session.execute(
                    text("SELECT comment_text FROM public.\"Comments\" WHERE comment_id = :comment ORDER BY id DESC;", comment=_id))
                comment_dt.append({_id: res_comm.first()})
            return comment_dt


class DataPreparation:

    @classmethod
    async def TaskDataLoader(cls, data_task, data_actions):
        dat_smp = {
            "comments": "",
            "statuses": "",
            "assignments": "",
            "task": data_task,
        }
        comm_dats = []
        stat_dats = []
        assign_dats = []
        for act in data_actions:
            if act[-1] is not None:
                comm = {"datetime": act[0],
                        "activity_id": act[2],
                        "master_id": act[-4],
                        "comment_id": act[-1],
                        "comment_text": await AlchemyMonster.get_task_comments_data((act[-1]),)}
                comm_dats.append(comm)
            if act[-2] is not None:
                stat = {"datetime": act[0],
                        "activity_id": act[2],
                        "master_id": act[-4],
                        "status_id": act[-2]}
                stat_dats.append(stat)
            if act[-3] is not None:
                assign = {"datetime": act[0],
                          "activity_id": act[2],
                          "master_id": act[-4],
                          "assignment_id": act[-3]}
                assign_dats.append(assign)
        dat_smp["comments"] = comm_dats
        dat_smp["statuses"] = stat_dats
        dat_smp["assignments"] = assign_dats
        return dat_smp
