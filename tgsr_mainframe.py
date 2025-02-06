from tracker.sr_manager import Forge, ts

Divisions = {
    "admin": "ADM",
    "123456": "TESTDIVISION"

}

items_aura = {"IssuerDivision": {
    "path": Divisions,
    "request": "UTID"
}
}


class aura:
    """
    AURA — service for autofill the requesting items by target table
    """

    def __init__(self):
        ...

    @staticmethod
    def __make_session(items_for_aura):
        session_id = Forge.uuid_generator()
        data = [ts(), session_id, items_for_aura, "WAIT"]
        print(f'MF_M2S DATA: {data}')
        return session_id

    @staticmethod
    def check_for_aura(items):
        for_tg = []
        for_aura = []
        session_id = 'without'
        item_id = 0
        for item in items:
            if item in list(items_aura.keys()):
                for_aura.append([item, item_id])
            else:
                for_tg.append(item)
            item_id += 1
        if len(for_aura) != 0:
            session_id = aura().__make_session(items_for_aura={"items": for_aura, "datascheme": items})
        for_tg.append(session_id)
        return for_tg

    @staticmethod
    def get_session_data(session_id):
        items_session = "ЗАПРОС К БД СЕССИЙ ПО SESSION ID. ДЛЯ ТЕСТА ВОЗВРАЩАЕМ СТАНДАРТ ДЛЯ запроса по %USR_NEW%"
        return {'items': [['IssuerDivision', 3]], 'datascheme': ['UTID', 'UserName', 'Issuer', 'IssuerDivision']}

    @staticmethod
    def session_worker(session_id, data):
        session_data = aura.get_session_data(session_id)
        for_back = []
        # print("MF___SESDATA", session_data)
        # print('MF___TGDATA ', data)
        items = session_data['items']
        # print("MF___ITEMS", items)
        for item in items:
            bs = items_aura[item[0]]
            number = get_index(session_data['datascheme'], bs['request'])
            ds_result = bs['path'][str(data[number])]
            for_back.append([item[1], ds_result])
        return for_back

    def aura_worker(self):
        ...


def get_index(data, item):
    """
    Func for find the index of target item

    :param data: array of items
    :param item: item to find the index
    :return: index of the target item
    """
    number = 0
    for dat in data:
        if dat != item:
            number += 1
        else:
            return number


class SR:
    def __init__(self):
        pass

    @classmethod
    def NewTaskPrep(cls, Thematic):
        NewPrep = Forge.GetProject(Thematic=Thematic, mode="ThematicKeys")
        return aura.check_for_aura(NewPrep)

    @classmethod
    def NewTask(cls, Thematic, data, session_id):
        """
        Class method to build the new dynamic sr-task
        :param Thematic: Thematic key. e.g. "USR_NEW"
        :param data: dynamic array, array template from SR.NewTaskPrep
        :param session_id: session_id from aura_handler
        :return:
        """
        dts = {}
        i = 0
        if session_id != 'without':
            data_ses = aura.session_worker(session_id, data)
            for ses in data_ses:
                data.insert(*ses)
        keys = Forge.GetProject(Thematic=Thematic, mode="ThematicKeys")
        num = get_index(keys, "Issuer")

        for key in keys:
            dts[key] = data[i]
            i += 1

        return Forge.NewSD(Thematic=Thematic, Issuer=data[num], data=dts)


