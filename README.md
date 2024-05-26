# Task list

>Steak:  
![Static Badge](https://img.shields.io/badge/FastAPI-0.111-brightgreen?style=flat-square&logo=FastAPI)
![Static Badge](https://img.shields.io/badge/Pydantic-2.7-brightgreen?style=flat-square&logo=Pydantic&labelColor=purple)
![Static Badge](https://img.shields.io/badge/Alembic-1.13-brightgreen?style=flat-square&logo=awsorganizations&labelColor=black)
![Static Badge](https://img.shields.io/badge/Uvicorn-2.29-brightgreen?style=flat-square&logo=gunicorn&logoColor=blue&labelColor=yellow)
![Static Badge](https://img.shields.io/badge/SQLalchemy-2.0-brightgreen?style=flat-square&logo=sqlalchemy&logoColor=black&labelColor=aliceblue)
![Static Badge](https://img.shields.io/badge/asyncpg-0.29-brightgreen?style=flat-square&logo=codeium&logoColor=black&labelColor=blue)

### Description
The application is completely asynchronous. The FastAPI library with asynchronous functions is used. For asynchronous interaction with the database, asyncpg is used.
The backend is written in FastAPI + Pydantic. created the main CRUD endpoints for tasks.
Added pydantic schemes for validating different types of tasks, as well as enum classes for fixed values.
The alembic is responsible for migrations.
The application runs on the standard uvicorn port.
Interaction with the database occurs through sqlalchemy.
A declarative writing style is used.

### Documentation

FastAPI Task Management Application
This application is designed to manage tasks with a PostgreSQL database. It supports CRUD operations along with search and pagination functionalities.

#### Models
- Task: Represents a task in the database.
- TagEnum: Enum for task tags.
- OrderingEnum: Enum for ordering tasks.
- AscDescEnum: Enum for sorting order.
---
#### Schemas
- TaskCreateSchema: Schema for creating a new task.
- TaskGetSchema: Schema for retrieving a task.
- TaskPatchSchema: Schema for partially updating a task.
- TaskPutSchema: Schema for fully updating a task.
---
#### Endpoints
___Get All Tasks___  
URL: /api/v1/tasks  
Method: GET  
Response Model: List[TaskGetSchema]  
Tags: ['GET']  
**Parameters:**
- limit (int): Number of tasks to return. Default is 10.
- offset (int): Number of tasks to skip. Default is 0.
- ordering (OrderingEnum): Field to order tasks by. Default is DATE.
- sort (AscDescEnum): Sorting order. Default is DESC.

**Description:**
Returns a paginated list of tasks from the database with optional sorting.

Get Completed Tasks
URL: /api/v1/tasks/completed
Method: GET
Response Model: List[TaskGetSchema]
Tags: ['GET']  
**Parameters:**
- limit (int): Number of tasks to return. Default is 10.
- offset (int): Number of tasks to skip. Default is 0.
- completed (bool): Filter tasks by completion status. Default is False.
- ordering (OrderingEnum): Field to order tasks by. Default is DATE.
- sort (AscDescEnum): Sorting order. Default is DESC.

**Description:**
Returns a paginated list of completed or not completed tasks from the database with optional sorting.

___Search Tasks___  
URL: /api/v1/tasks/search  
Method: GET  
Response Model: List[TaskGetSchema]  
Tags: ['GET']  
**Parameters:**

- limit (int): Number of tasks to return. Default is 10.
- offset (int): Number of tasks to skip. Default is 0.
- search (str): Search query to filter tasks by title or description.
- ordering (OrderingEnum): Field to order tasks by. Default is DATE.
- sort (AscDescEnum): Sorting order. Default is DESC.

**Description:**
Returns a paginated list of tasks that match the search query in the title or description, with optional sorting.

___Get Task by ID___  
URL: /api/v1/tasks/{task_id}  
Method: GET  
Response Model: TaskGetSchema  
Tags: ['GET']  
**Parameters:**

- task_id (int): ID of the task to retrieve.

**Description:**
Returns a task by its ID.

___Create Task___  
URL: /api/v1/tasks  
Method: POST  
Response Model: TaskGetSchema  
Status Code: 201  
Tags: ['POST']  
**Body:**

- task (TaskCreateSchema): The task data to create.
- tags (TagEnum, optional): Tag for the task.

**Description:**
Creates a new task in the database.

___Toggle Task Completion___  
URL: /api/v1/tasks/{task_id}/completed/  
Method: PATCH  
Response Model: TaskGetSchema  
Tags: ['PATCH']  
**Parameters:**

- task_id (int): ID of the task to toggle completion status.

**Description:**
Toggles the completion status of a task.

___Partially Update Task___  
URL: /api/v1/tasks/{task_id}  
Method: PATCH  
Response Model: TaskGetSchema  
Tags: ['PATCH']  
**Parameters:**

- task_id (int): ID of the task to update.
- task (TaskPatchSchema): The task data to update. 

**Description:**
Partially updates a task's fields. Only the fields provided will be updated.

___Fully Update Task___  
URL: /api/v1/tasks/{task_id}  
Method: PUT  
Response Model: TaskGetSchema  
Tags: ['PUT']  
**Parameters:**

- task_id (int): ID of the task to update.
- task (TaskPutSchema): The task data to update.

**Description:**
Fully updates a task's fields. All fields must be provided.

___Delete Task___  
URL: /api/v1/tasks/{task_id}  
Method: DELETE  
Tags: ['DELETE']  
**Parameters:**

- task_id (int): ID of the task to delete.

**Description:**
Deletes a task by its ID.