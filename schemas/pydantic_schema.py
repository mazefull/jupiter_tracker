from typing import Optional, Any
from pydantic import BaseModel, Field


class BaseSchema(BaseModel):
    master_id: str = Field(min_length=7, max_length=9, pattern=r"[R]\d-\w{6}")  # 'R1-JP1GH2'


class EditSchema(BaseSchema):
    task_id: str = Field(pattern=r"[XT]-\w{8}")


class SRActivityAddSchema(BaseSchema):
    # activity_id: str = Field(min_length=12, max_length=12)
    task_id: str = Field(min_length=12, max_length=36)
    activity_id: str = Field(min_length=12, max_length=12)
    assignment_id: Optional[str] = Field(default=None, max_length=12)
    status_id: Optional[str] = Field(default=None, max_length=12)
    comment__id: Optional[str] = Field(default=None, max_length=12)


class SRTaskAddSchema(BaseSchema):
    project_id: str = Field(min_length=3, max_length=12)
    thematic_id: str = Field(min_length=3, max_length=12)
    assignee_master_id: Optional[str] = Field(default='R1-JP1GH2', pattern=r"[R]\d-\w{6}")
    data: dict[str, Any]


class SRStatusAddSchema(EditSchema):
    status: str = Field(min_length=3, max_length=12)


class SRCommentAddSchema(EditSchema):
    comment_text: str = Field(min_length=3, max_length=100)


class SRAssignmentAddSchema(EditSchema):
    assignee_master_id: str = Field(min_length=12, max_length=12, pattern=r"[R]\d-\w{6}")


class SRActionWizardAddSchema(EditSchema):
    status: Optional[str] = Field(min_length=3, max_length=12)
    comment_text: Optional[str] = Field(min_length=3, max_length=100)
    assignee_master_id: Optional[str] = Field(min_length=12, max_length=12, pattern=r"[R]\d-\w{6}")


class UserAddSchema(BaseSchema):
    tg_id: int = Field(min_length=5, max_length=12)
    user_status: str = Field(min_length=3, max_length=12, default='NEW')
    user_primary_group: Optional[str] = Field(min_length=5, max_length=12, pattern=r"^acc_\w*", default="acc_none")
    user_secondary_group: Optional[str] = Field(min_length=5, max_length=12, pattern=r"^acc_\w*", default="acc_none")
