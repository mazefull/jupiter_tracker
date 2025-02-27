from watchfiles import awatch

from schemas.pydantic_schema import SRActionWizardAddSchema, SRTaskAddSchema
from schemas.project_schema import data_schema, projects
from services.activity_service import ActivityService, Validators
from services.task_builder import Builder


class CustomObject:
    def __init__(self, param_dict):
        for key, value in param_dict.items():
            setattr(self, key, value)


async def ThematicValidation(thematic: str):
    projects_list = list(projects.keys())
    project = (str(thematic).split('_'))[0]
    if project in projects_list:
        if thematic in projects[project]['issues_thematics'].keys():
            return project, thematic
        return False, thematic
    return False, thematic


async def DataValidation(data: dict, project: str, thematic: str):
    template_name = await GetSpecialDataTemplateName(project, thematic)

    if not template_name[0]:
        return template_name

    template = await GetSpecialDataTemplate(template_name[1])
    if not template[0]:
        return template

    elif template[1].keys() == data.keys():
        return True, 'ok'
    return False, f'Incorrect template data, must be in format {template[1]}'


async def GetSpecialDataTemplateName(project: str, thematic: str):
    try:
        return True, projects[project]['issues_thematics'][thematic]['schema']
    except KeyError:
        return False, 'Incorrect project'


async def GetSpecialDataTemplate(template_name: str):
    try:
        return True, data_schema[template_name]
    except:
        return False, 'No data schema for project'


class ManagerService:
    @classmethod
    async def new_task(cls, task: SRTaskAddSchema):
        validation = await DataValidation(task.data, task.project_id, task.thematic_id)

        if validation[0]:
            master_activity = await ActivityService.MainWizard(master_id=task.master_id, interface=task.system)
            return await Builder.TaskBuilder(task, master_activity)
        return {"ok": validation[0], "details": validation[1]}

    @classmethod
    async def get_projects_data(cls):
        thema = {}
        for project in projects.keys():
            thema[project] = list(projects[project]['issues_thematics'].keys())
        return thema

    @classmethod
    async def task_multi_action(cls, wizard: SRActionWizardAddSchema):
        # await Validators.GetTaskData(wizard.task_id)
        if await Validators.IsTaskExsist(wizard.task_id):
            master_activity = await ActivityService.MainWizard(master_id=wizard.master_id, interface=wizard.system)
            return await(Builder.MultiActionWizard(wizard, master_activity))
        return {"ok": False, "details": 'Incorrect task id'}

    async def new_project(self, data):
        ...


class ManagerSD:
    async def new_sd(self, sd):
        ...
