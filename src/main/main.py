from fastapi import FastAPI, Body, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.main.schemas import TagEnum, TaskCreateSchema, TaskGetSchema
from src.database.models import Task

from src.database.connect import get_session

app = FastAPI()


@app.get('/', response_model=list[TaskGetSchema])
async def get_all_task(session: AsyncSession = Depends(get_session)):
    async with session as s:
        result = await s.execute(select(Task))
        tasks = result.scalars().all()
        return tasks


@app.post('/')
async def add_task(tags: TagEnum = None, task: TaskCreateSchema = Body(...),
                   session: AsyncSession = Depends(get_session)):
    cur_tusk = Task(**task.dict(), tags=tags.value if tags else None)
    async with session as s:
        s.add(cur_tusk)
        await s.commit()
    return cur_tusk
