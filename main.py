from db import svc
from tgsr_mainframe import SR




task_prep = SR.NewTaskPrep('USR_NEW')
print("MAIN: ", task_prep)
TaskID = SR.NewTask(Thematic='USR_NEW', data=[123456, 'TESTUNAME', 'TESTISSUER'], session_id=task_prep[-1])
print("TASKOID: ", TaskID)


# Forge.MultiAction(15561, 16156, 8944, ['TEXT' , 894844], 84986)