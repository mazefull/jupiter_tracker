# from (deprecated) import svc
# from tgsr_mainframe import SR
from pydantic_settings import BaseSettings, SettingsConfigDict
from main1 import app

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()



















# task_prep = SR.NewTaskPrep('USR_NEW')
# print("MAIN: ", task_prep)
# TaskID = SR.NewTask(Thematic='USR_NEW', data=[123456, 'TESTUNAME', 'TESTISSUER'], session_id=task_prep[-1])
# print("TASKOID: ", TaskID)