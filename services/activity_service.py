from sqlalchemy import update, select
from services.utils import ts, uuidg
from models.data_models import MasterActivity
from db.db import new_session


class ActivityService:
    @classmethod
    async def MainWizard(cls, master_id: str, interface: str):
        mdata = MasterActivity(
            datetime=ts(),
            activity_id=uuidg("MGA-"),
            activity_slave_id=None,
            master_id=master_id,
            interface=interface,
        )
        if await AlchemyMonster(models=(mdata,)).am_add():
            return mdata.activity_id

    @classmethod
    async def UpdateMain(cls, master_activity, slave_activity):
        mdata = MasterActivity(
            activity_id=master_activity,
            activity_slave_id=slave_activity,
        )
        return await AlchemyMonster(models=mdata).insert_slave()


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
                await session.rollack()
                return False

    async def insert_slave(self):
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
            else:
                return False
