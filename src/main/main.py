from fastapi import FastAPI, Body, Depends, HTTPException
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.main.schemas import TagEnum, TaskCreateSchema, TaskGetSchema, TaskPatchSchema, TaskPutSchema, OrderingEnum, \
    AscDescEnum
from src.database.models import Task

from src.database.connect import get_session

app = FastAPI()


@app.get('/api/v1/tasks', response_model=list[TaskGetSchema], tags=['GET'])
async def get_all_task(limit: int = 10, offset: int = 0, session: AsyncSession = Depends(get_session),
                       ordering: OrderingEnum = OrderingEnum.DATE, sort: AscDescEnum = AscDescEnum.DESC):
    """
    The function returns all records on a page from the database.
    With option to sort by OrderingEnum
    """
    async with session as s:
        result = await s.execute(
            select(Task).offset(offset).limit(limit).order_by(
                getattr(Task, ordering.value).desc() if sort.value == 'desc()' else getattr(Task, ordering.value))
        )
        query = result.scalars().all()
        if query:
            return query
        else:
            raise HTTPException(status_code=404, detail='Task not found')


@app.get('/api/v1/tasks/completed', response_model=list[TaskGetSchema], tags=['GET'])
async def get_completed_task(session: AsyncSession = Depends(get_session), ordering: OrderingEnum = OrderingEnum.DATE,
                             limit: int = 10, offset: int = 0, completed: bool = False,
                             sort: AscDescEnum = AscDescEnum.DESC):
    """
    The function returns all records on a page from the database where completed
    With option to sort by OrderingEnum
    """
    async with session as s:
        result = await s.execute(select(Task).where(Task.completed == completed).limit(limit).offset(offset).order_by(
            getattr(Task, ordering.value).desc() if sort.value == 'desc()' else getattr(Task, ordering.value)
        ))
        query = result.scalars().all()
        if query:
            return query
        else:
            raise HTTPException(status_code=404, detail='Task not found')


@app.get('/api/v1/tasks/search', response_model=list[TaskGetSchema], tags=['GET'])
async def get_task_by_title(limit: int = 10, offset: int = 0, search: str = None,
                            session: AsyncSession = Depends(get_session),
                            ordering: OrderingEnum = OrderingEnum.DATE, sort: AscDescEnum = AscDescEnum.DESC):
    """
    The function returns all records on a page from the database where search query
    Search is carried out by title and description
    With option to sort by OrderingEnum
    """
    async with session as s:
        if search:
            result = await s.execute(
                select(Task).where(or_(Task.title.contains(search), Task.description.contains(search))).offset(
                    offset).limit(limit).order_by(
                    getattr(Task, ordering.value).desc() if sort.value == 'desc()' else getattr(Task, ordering.value))
            )
        else:
            result = await s.execute(
                select(Task).offset(offset).limit(limit).order_by(
                    getattr(Task, ordering.value).desc() if sort.value == 'desc()' else getattr(Task, ordering.value))
            )
        query = result.scalars().all()
        if query:
            return query
        else:
            raise HTTPException(status_code=404, detail='Task not found')


@app.get('/api/v1/tasks/{task_id}', response_model=TaskGetSchema, tags=['GET'])
async def get_task(task_id: int, session: AsyncSession = Depends(get_session)):
    """
    The function returns a task by id
    """
    async with session as s:
        result = await s.execute(select(Task).where(Task.id == task_id))
        query = result.scalars().first()
        if query:
            return query
        else:
            raise HTTPException(status_code=404, detail='Task not found')


@app.post('/api/v1/tasks', status_code=201, response_model=TaskGetSchema, tags=['POST'])
async def add_task(tags: TagEnum = None, task: TaskCreateSchema = Body(...),
                   session: AsyncSession = Depends(get_session)):
    """
    The function adds a new task
    """
    cur_tusk = Task(**task.dict(), tags=tags.value if tags else None)
    async with session as s:
        s.add(cur_tusk)
        await s.commit()
    return cur_tusk


@app.patch('/api/v1/tasks/{task_id}/completed/', response_model=TaskGetSchema, tags=['PATCH'])
async def patch_completed_task(task_id: int, session: AsyncSession = Depends(get_session)):
    """
    The function changes the status of the task
    """
    async with session as s:
        result = await s.execute(select(Task).where(Task.id == task_id))
        task = result.scalars().first()
        if task:
            task.completed = not task.completed
            await s.commit()
            await s.refresh(task)
            return task
        else:
            raise HTTPException(status_code=404, detail='Task not found')


@app.patch('/api/v1/tasks/{task_id}', response_model=TaskGetSchema, tags=['PATCH'])
async def patch_task(task_id: int,
                     task: TaskPatchSchema = Body(...),
                     session: AsyncSession = Depends(get_session)):
    """
    you can pass arbitrary fields, and the number of fields
    """
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


@app.put('/api/v1/tasks/{task_id}', response_model=TaskGetSchema, tags=['PUT'])
async def update_task(task_id: int,
                      task: TaskPutSchema = Body(...),
                      session: AsyncSession = Depends(get_session)):
    """
    function updates all fields of task
    """
    async with session as s:
        result = await s.execute(select(Task).where(Task.id == task_id))
        task_bd = result.scalars().first()
        update = task.dict(exclude_unset=True)
        for k, v in update.items():
            setattr(task_bd, k, v)
        s.add(task_bd)
        await s.commit()
        await s.refresh(task_bd)
        return task_bd


@app.delete('/api/v1/tasks/{task_id}', tags=['DELETE'])
async def delete_task(task_id: int, session: AsyncSession = Depends(get_session)):
    """
    The function deletes a task
    """
    async with session as s:
        result = await s.execute(select(Task).where(Task.id == task_id))
        task = result.scalars().first()
        if task:
            await s.delete(task)
            await s.commit()
            return {'deleted': True, 'object': task}
        else:
            raise HTTPException(status_code=404, detail='Task not found')
