from fastapi import FastAPI, Body, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.main.schemas import TagEnum, TaskCreateSchema, TaskGetSchema, TaskPatchSchema
from src.database.models import Task

from src.database.connect import get_session

app = FastAPI()


@app.get('/api/v1/tasks', response_model=list[TaskGetSchema])
async def get_all_task(session: AsyncSession = Depends(get_session)):
    async with session as s:
        result = await s.execute(select(Task))
        tasks = result.scalars().all()
        return tasks


@app.post('/api/v1/tasks', status_code=201, response_model=TaskGetSchema)
async def add_task(tags: TagEnum = None, task: TaskCreateSchema = Body(...),
                   session: AsyncSession = Depends(get_session)):
    cur_tusk = Task(**task.dict(), tags=tags.value if tags else None)
    async with session as s:
        s.add(cur_tusk)
        await s.commit()
    return cur_tusk


@app.get('/api/v1/tasks/{task_id}', response_model=TaskGetSchema)
async def get_task(task_id: int, session: AsyncSession = Depends(get_session)):
    async with session as s:
        result = await s.execute(select(Task).where(Task.id == task_id))
        if result:
            task = result.scalars().first()
            return task
        else:
            raise HTTPException(status_code=404, detail='Task not found')


@app.patch('/api/v1/tasks/{task_id}', response_model=TaskGetSchema)
async def patch_task(task_id: int,
                      task: TaskPatchSchema = Body(...),
                      session: AsyncSession = Depends(get_session)):
    async with session as s:
        result = await s.execute(select(Task).where(Task.id == task_id))
        task_bd = result.scalars().first()
        update = task.dict(exclude_unset=True)
        for k, v in update.items():
            if v:
                setattr(task_bd, k, v)
        s.add(task_bd)
        await s.commit()
        await s.refresh(task_bd)
        return task_bd


# @app.put('/api/v1/tasks/{task_id}', response_model=TaskGetSchema)
# async def update_task(task_id: int,
#                       task: TaskPatchSchema = Body(...),
#                       session: AsyncSession = Depends(get_session)):