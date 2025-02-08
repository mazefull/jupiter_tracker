data_schema = {
    "usr_newact": {
        "target": "",
        "Issuer": ""
    },
    "usr_newact1": {
        "target": 2,
        "Issuer": 3
    }
}


projects = {
    'USR': {
        'tittle': 'USER MANAGEMENT',
        'root': 0,
        'project_id': 2,
        'issues_thematics': {
            'NEW': {
                'tittle': 'NEW USER ACTIVATION',
                'root': 1,
                'thematics_id': "P2R1T0",
                'schema': 'usr_newact',
                'start_assigner': 'acc_admin',
                'description': 'APPLY ACCESS TO SYSTEM? CHOSE ROLE'
            },
            "NEW1": "NONE"
        }
    },
    "TEST": {
        "tittle": "TEST TITTLE",
        'issues_thematics': {
            "test": "None"
        }
    }
}
