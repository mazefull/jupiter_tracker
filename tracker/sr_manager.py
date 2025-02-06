from db.svc import db, cur
from uuid import uuid4
from datetime import datetime as dt


def ts():
    a = dt.now().strftime("%Y-%m-%d %H:%M:%S")
    return a


projects = {
    "projects": {
        'VPN': {
            'tittle': 'VPN ISSUES',
            'root': 0,
            'project_id': 1,
            'issues_thematics': {
                'VPN_NEW': {
                    'tittle': 'ADD VPN USER',
                    'root': 1,
                    'thematics_id': "P1R1T0",
                    'schema': 'vpn_newuser'
                },
                'VPN_ERRS': {
                    'tittle': 'PROBLEM WITH VPN',
                    'root': 1,
                    'thematics_id': "P1R1T1",
                    'schema': 'vpn_problem'
                },
                'VPN_DEL': {
                    'tittle': 'DEL VPN USER',
                    'root': 1,
                    'thematics_id': "P1R1T2",
                    'schema': 'vpn_deluser'
                },
                'VPN_FB': {
                    'tittle': 'VPN Q/FEEDBACK',
                    'root': 1,
                    'thematics_id': "P1R1T3",
                    'schema': 'vpn_feedback'
                }
            }
        },
        'USR': {
            'tittle': 'USER MANAGEMENT',
            'root': 0,
            'project_id': 2,
            'issues_thematics': {
                'USR_NEW': {
                    'tittle': 'NEW USER ACTIVATION',
                    'root': 1,
                    'thematics_id': "P2R1T0",
                    'schema': 'usr_newact',
                    'start_assigner': 'acc_admin',
                    'description': 'APPLY ACCESS TO SYSTEM? CHOUSE ROLE'
                },
                'USR_CHPROLE': {
                    'tittle': 'USER CHANGE PRIMARY ROLE',
                    'root': 1,
                    'thematics_id': "P2R1T1",
                    'schema': 'usr_chrole_primary'
                },
                'USR_CHROLE': {
                    'tittle': 'USER CHANGE CLASSIC ROLE',
                    'root': 1,
                    'thematics_id': "P2R1T2",
                    'schema': 'usr_chrole'
                },
                'USR_PROJ_ACC': {
                    'tittle': 'USER MGMT PROJECT ACCESS',
                    'root': 1,
                    'thematics_id': "P2R1T3",
                    'schema': 'usr_proj_acc'
                },
                'USR_MGMT': {
                    'tittle': 'USER MGMT MASTER',
                    'root': 1,
                    'thematics_id': "P2R1T4",
                    'schema': 'usr_mgmt_master'
                }
            }
        },
        'INTERNAL': {
            'tittle': 'INTERNAL SYSTEMS AUTO_TASK',
            'root': 0,
            'project_id': 3,
            'issues_thematics': {
                'INTERNAL_MASTE': {
                    'tittle': 'INTERNAL_',
                    'root': 1,
                    'thematics_id': "P2R1T0",
                    'schema': 'internal_cc',
                    'start_assigner': 'cc_mainframe',
                    'description': 'insignia unique task. NO_DESCRIPTION'
                }
            }
        },
        'GROUP': {
            'tittle': 'USER MANAGEMENT',
            'root': 0,
            'project_id': 2,
            'issues_thematics': {
                'GROUP_UREQ': {
                    'tittle': 'MASS USER REQUEST',
                    'root': 1,
                    'thematics_id': "P2R1T0",
                    'schema': 'group_req',
                    'start_assigner': 'acc_group_*',
                    'description': '**'
                }



            }




        }
    }
}

projects_schema = {
        'usr_newact': {
            'UTID': '',
            'UserName': '',
            'Issuer': '',
            'IssuerDivision': ''
        },
        'group_req': {  #Создаёт эпик запрос, в рамках которого задача назначается на группу юзеров.
            # При отсутсвии базовой группы, создаётся новая сущность с наименованием %acc_group_temp_$UID%
            '*UTGROUP': '',  #При отсутствии группы, пользователи выбираются вручную, также при недостаточности текущей
            # группы, к ней вручную добавляются юзеры, и, либо обновляется текущая группа(!!!APLLY ADMIN), либо создаётся temp-сущность.
            '**Descriprion': '',
            'svc_apply': '',  #Сервис функция Apply/descard.
            'Issuer': '',
            'IssuerDivision': ''
        }
}

project_action_schema = {


}


class Forge:

    def __init__(self):
        pass

    @classmethod
    def uuid_generator(cls):
        uuid_short = str(uuid4())[-12:]
        # uuid_short = str(uuid4())
        return uuid_short

    @classmethod
    def long_uuid(cls):
        return str(uuid4())

    def ActivityBuilder(self):
        pass

    def __GetProjectInfoByKey(self, project, key=None):
        project_data = projects['projects'][project]
        if not key:
            print(project_data)
        else:
            print(project_data[key])


    def __GetStartAssigner(self, Thematic):
        proj = (self.IsThematicExsist(Thematic))[1]
        return projects['projects'][proj]['issues_thematics'][Thematic]['start_assigner']

    def __GetThematicInformation(self, pr_them):
        thematic_data = projects['projects'][pr_them[1]]['issues_thematics'][pr_them[2]]
        return thematic_data

    def IsThematicExsist(self, thematic):
        projects_list = list(projects['projects'].keys())
        project = (str(thematic).split('_'))[0]
        if project in projects_list:
            return True, project, thematic
        else:
            return None

    def __GetThematicSchemaData(self, Thematic):
        predata = self.IsThematicExsist(Thematic)
        if predata is not None:
            ThematicSchema = projects['projects'][predata[1]]['issues_thematics'][predata[2]]['schema']
            ThematicSchemaData = self.__GetSDTemplate(ThematicSchema)
            return ThematicSchemaData


    def __GetSDTemplate(self, schema):
        try:
            schema = projects_schema[schema]
        except:
            schema = None
        return schema

    def __NewActivity(self, DateTime, TaskID, ActivityIssuer, NewAssigner=None, NewStatus=None, NewComment=None):
        """
        :param TaskID: полный ID таска
        :param ActivityIssuer: Создатель активности
        :param NewAssigner: str(UTID) or str(TaskGroup)
        :param NewStatus: str
        :param NewComment: [CommentText, CommentHolder]
        :return:
        """
        ActivityID = self.uuid_generator()
        NewAssignerID, NewStatusID, NewCommentID = None, None, None
        if NewAssigner is not None:
            NewAssigner = self.__NewAssign(DateTime, ActivityID, TaskID, NewAssigner)
            NewAssignerID = NewAssigner[-1]
        if NewStatus is not None:
            NewStatus = self.__NewStatus(DateTime, ActivityID, TaskID, NewStatus)
            NewStatusID = NewStatus[-1]
        if NewComment is not None:
            NewComment = self.__NewComment(DateTime, ActivityID, TaskID, NewComment[0], NewComment[1])
            NewCommentID = NewComment[-1]
        NewAction = [DateTime, ActivityID, TaskID, ActivityIssuer, NewAssignerID, NewStatusID, NewCommentID]

        return [NewAction, NewAssigner, NewStatus, NewComment]
        # return {"Action": NewAction, "Assigner": NewAssigner, "Status": NewStatus, "Comment": NewComment}

    def __NewStatus(self, DateTime, ActivityID, TaskID, NewStatus):
        return [DateTime, ActivityID, TaskID, NewStatus, self.uuid_generator()]


    def __NewComment(self, DateTime, ActivityID, TaskID, NewCommentText, CommentHolder):
        return [DateTime, ActivityID, TaskID, NewCommentText, CommentHolder, self.uuid_generator()]


    def __NewAssign(self, DateTime, ActivityID, TaskID, NewAssigner):
        return [DateTime, ActivityID, TaskID, NewAssigner, self.uuid_generator()]


    def __GetThematicLastTaskNum(self):
        return 0


    def __GetTaskID(self, TaskOID):
        """
        Получаем значение ID задания по Внешнему ID таска
        :param TaskOID:
        :return:
        """
        return 100

    def __GetTaskKID(self, TaskID):
        """
        Получаем внешний ID таска по ID задания
        :param TaskID:
        :return:
        """
        return 101

    def __NewSDBuilder(self, Thematic, ThematicInformation, ThematicSchema, Issuer, data=None):
        print(f'{Thematic}\n{ThematicInformation}\n{ThematicSchema}')
        DateTime = ts()
        if True:
            TaskID = self.long_uuid()
            TaskOID = f'{Thematic[2]}-{int(self.__GetThematicLastTaskNum())+1}'
            NewActivityData = self.__NewActivity(DateTime, TaskID, Issuer, NewAssigner=self.__GetStartAssigner(Thematic[2]), NewStatus="NEW")
            NewTaskData = [DateTime, TaskID, TaskOID, NewActivityData[0][1], Thematic[2], "NEW", Issuer, data]
            print(f"NewActivityData: {NewActivityData}\nNewTaskData: {NewTaskData}")
            self.__send_transaction(*[NewTaskData, *NewActivityData])

            return TaskOID


    def __GetKeysThematicForSendSD(self, Thematic):
        ThematicSchemaData = self.__GetThematicSchemaData(Thematic)
        s = list(ThematicSchemaData.keys())
        # print(s)
        return list(ThematicSchemaData.keys())


    @classmethod
    def teststart(self, thematic):
        res = Forge().IsThematicExsist(thematic)
        if res[0]:
            print(res)
            Forge().__GetThematicInformation(res)
        else:
            print(res)

    @classmethod
    def NewSD(self, Thematic, Issuer, data):
        '''
        special_data должна быть в формате словаря по ключам тематики запроса {}.
        Ключи тематики запроса можно получить
        :param Thematic:
        :return:
        '''
        ThematicCheck = Forge().IsThematicExsist(Thematic)
        if ThematicCheck[0] is False:
            print('INCORRECT THEMATIC')
        else:
            ThematicInformation = Forge().__GetThematicInformation(ThematicCheck)
            ThematicSchema = Forge().__GetSDTemplate(ThematicInformation['schema'])
            if ThematicSchema is None:
                print('No SCHEMA FORTHEMATIC')
            else:
                TaskOID = Forge().__NewSDBuilder(ThematicCheck, ThematicInformation, ThematicSchema, Issuer, data)
                return TaskOID

        # sd_task_id = self.__NewActivity(thematic, assigner, issuer)

    @classmethod
    def GetProject(self, Project=None, Thematic=None, mode=None):
        """
        С помощью данного метода можно получить список всех проектов, тематик, а также заголовок тематики
        :param Project: Название проекта
        :param Thematic: Название тематики
        :param mode: Может принимать значения None, ThematicList, ThematicTittle, ThematicKeys
        :return:
        """
        if not mode:
            return list(projects['projects'].keys())
        elif mode == 'ThematicList':
            try:
                return list(projects['projects'][Project]['issues_thematics'].keys())
            except:
                return "Incorrect Project or No Project"
        elif mode == 'ThematicTittle':
            project = self().IsThematicExsist(thematic=Thematic)
            try:
                return projects['projects'][project[1]]['issues_thematics'][Thematic]['tittle']
            except:
                return "Incorrect Thematic or No Thematic"
        elif mode == 'ThematicKeys':
            try:
                return self().__GetKeysThematicForSendSD(Thematic=Thematic)
            except:
                return None

    @classmethod
    def MultiAction(cls, TaskID, ActivityIssuer, NewAssign=None, NewComment=None, NewStatus=None):
        data = cls().__NewActivity(DateTime=ts(),
                                   TaskID=TaskID,
                                   ActivityIssuer=ActivityIssuer,
                                   NewAssigner=NewAssign,
                                   NewComment=NewComment,
                                   NewStatus=NewStatus)
        print(data)


    def __send_transaction(self, data_task, data_action, data_assigner, data_status, data_comment):
        if data_task is not None:
            print('SEND TRANS TASK ', data_task)
        if data_action is not None:
            print('SEND TRANS ACTION ', data_action)
        if data_assigner is not None:
            print('SEND TRANS ASSIGNER ', data_assigner)
        if data_status is not None:
            print('SEND TRANS STATUS ', data_status)
        if data_comment is not None:
            print('SEND TRANS COMMENT ', data_comment)

        trans_uuid = self.uuid_generator()
        print('TRANS UID: ', trans_uuid)




    @classmethod
    class EditSD:

        def __init__(self):
            pass

        def ChangeStatus(self):
            pass

        def ChangeAssigner(self):
            pass

        def AddComment(self):
            pass

        def MultiAction(self):
            pass

