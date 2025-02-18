import {useState} from "react";
import { Button, Form, Input, Radio } from 'antd';
import {ResetDataBase, ExecuteNewTask } from "./Endpoins.jsx"

function TaskMenu() {
    const [count, setCount] = useState(0)
    const [form] = Form.useForm();
    const [formInputsWidth, setFormInputsWidth] = useState('30%');


    const onClick = () => {
        let project_id;
        let thematic_id;
        let master_id;
        let assignee_master_id;
        let data;
        let system;
        project_id = form.getFieldValue(["project_id"])
        thematic_id = form.getFieldValue(["thematic_id"])
        master_id = form.getFieldValue(["master_id"])
        assignee_master_id = form.getFieldValue(["assignee_master_id"])
        data = JSON.parse(form.getFieldValue(["special_data"]))
        system = "WEB"

        ExecuteNewTask(project_id, thematic_id, master_id, assignee_master_id, data, system)

    };
    const onResetDBButton = () => {
        ResetDataBase()

    }

    return (
<>
    <Form
        layout={'horizontal'}
        form={form}
        tittle={'Task'}
    >
        <Form.Item label="NEW TASK FORM">
        </Form.Item>
        <Form.Item
            label="Project ID" style={{ width: formInputsWidth }} name="project_id">
            <Input placeholder="Task Project" />
        </Form.Item>
        <Form.Item label="Thematic ID" style={{ width: formInputsWidth }} name="thematic_id">
            <Input placeholder="Task Thematic" />
        </Form.Item>
        <Form.Item label="Master ID" style={{ width: formInputsWidth }} name="master_id">
            <Input placeholder="Your master ID" />
        </Form.Item>
        <Form.Item label="Assignee" style={{ width: formInputsWidth }} name="assignee_master_id">
            <Input placeholder="Optional" />
        </Form.Item>
        <Form.Item label="Special Data" style={{ width: formInputsWidth }} name="special_data">
            <Input placeholder='{"key0":"value0","key1":"value1"...}'/>
        </Form.Item>
        <Form.Item>
            <Button
                onClick={onClick}
                type="primary"
            >Submit</Button>
        </Form.Item>
        <Form.Item>
            <Button
                onClick={onResetDBButton}
                type="primary"
                danger={true}
                autoInsertSpace={true}
            >RESET_DB</Button>
        </Form.Item>
    </Form>
</>
    )

}

export default TaskMenu