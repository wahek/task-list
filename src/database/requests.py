# from fastapi import Depends
# from sqlalchemy import select
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from src.database.connect import get_session
# from src.database.models import Task
#
#
# async def get_task_by_id(task_id: int, session: AsyncSession = Depends(get_session)):
#     async with session as s:
#         res = await s.execute(select(Task).where(Task.id == task_id))
#         return res.scalars().first()

