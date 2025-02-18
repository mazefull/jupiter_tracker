import axios from "axios";

export const ExecuteNewTask = (project_id, thematic_id, master_id, assignee_master_id, data, system) => {
    axios.post('http://127.0.0.1:8000/tasks/new_task',
        {project_id, thematic_id, master_id, assignee_master_id, data, system},
        {headers: {'accept': 'application/json',
                'Content-Type': 'application/json'}}
    ).then((res) => {
        console.log("RESPONSE: ", res.data, " ", res.status)
        if (res.data["ok"] === true) {
            alert(`Создан запрос: ${res.data["task_id"]}`)
        }
        else {
            alert(`Ошибка при создании запроса`)

        }
    })
}
export const ResetDataBase =  () => {
    axios.post('http://127.0.0.1:8000/tasks/setup_db',
        {},
        {headers:
                {'accept': 'application/json',
                    'Content-Type': 'application/json'}}).then((res) => {
        console.log("RESPONSE: ", res.data["detail"])
        if (res.status === 200) {
            alert(`БД создана заново`)
        }
    })
}