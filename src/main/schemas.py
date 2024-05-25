from pydantic import BaseModel, Field

from datetime import datetime, timedelta
from enum import Enum


class TagEnum(Enum):
    URGENT = "urgent"
    IMPORTANT = "important"
    OPTIONAL = "optional"


class TaskGetSchema(BaseModel):
    id: int
    title: str
    description: str
    deadline: datetime | None
    tags: TagEnum | None
    completed: bool
    date_created: datetime


class TaskCreateSchema(BaseModel):
    title: str = Field(max_length=100, title="Task title")
    description: str = Field(title="description of task (no limit)")
    deadline: datetime | None = Field(title="deadline of task", default=None)
    tags: TagEnum | None = Field(title="tag of task", default=None)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "task",
                    "description": "description of task",
                    "deadline": (datetime.now() + timedelta(days=1)).replace(microsecond=0),
                }
            ]
        },
    }


class TaskPatchSchema(BaseModel):

    title: str | None = Field(max_length=100, title="Task title", default=None)
    description: str | None = Field(title="description of task (no limit)", default=None)
    deadline: datetime | None = Field(title="deadline of task", default=None)
    tags: TagEnum | None | str = Field(title="tag of task", default=None)
    completed: bool | None = Field(default=None)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": None,
                    "description": None,
                    "deadline": None,
                    "tags": None,
                    "completed": None,
                }
            ]
        },
    }


class TaskPutSchema(BaseModel):

    title: str | None = Field(max_length=100, title="Task title")
    description: str | None = Field(title="description of task (no limit)")
    deadline: datetime | None = Field(title="deadline of task", default=None)
    tags: TagEnum | None | str = Field(title="tag of task", default=None)
    completed: bool = Field(default=False)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": None,
                    "description": None,
                    "deadline": None,
                    "tags": None,
                    "completed": None,
                }
            ]
        },
    }
