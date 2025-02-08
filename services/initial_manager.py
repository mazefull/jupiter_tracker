from schemas.pydantic_schema import SRActionWizardAddSchema
from schemas.project_schema import data_schema, projects
from services.task_builder import Builder, v, setv


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
        else:
            return False, thematic
    else:
        return False, thematic


async def DataValidation(data: dict, project: str, thematic: str):
    template_name = await GetSpecialDataTemplateName(project, thematic)
    template = await GetSpecialDataTemplate(template_name)
    if not template:
        pass
    elif template.keys() == data.keys():
        setv(True)
    else:
        setv(False, "Special data haven't mandatory template_keys")


async def GetSpecialDataTemplateName(project: str, thematic: str):
    try:
        return projects[project]['issues_thematics'][thematic]['schema']
    except KeyError:
        setv(False, "Project/Thematic not found")


async def GetSpecialDataTemplate(template_name: str):
    try:
        return data_schema[template_name]
    except:
        setv(False, "No such template")


class ManagerService:
    async def new_task(self, task):
        print(task)
        await DataValidation(task.data, task.project_id, task.thematic_id)
        if v.status:
            return await Builder.TaskBuilder(task)
        else:
            return v

    async def get_projects_data(self):
        thema = {}
        for project in projects.keys():
            thema[project] = list(projects[project]['issues_thematics'].keys())
        return thema

    async def new_project(self, data):
        ...

    async def wizard(self, data: SRActionWizardAddSchema):
        master_id = data.master_id
