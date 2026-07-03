from factory import api, db
from spectree import Response
from flask import request, Blueprint
from flask_jwt_extended import jwt_required, current_user
from models.study_task import StudyTask, StudyTaskResponse, StudyTaskRequest, StudyTaskUpdateRequest
from models.subject import Subject
from utils.response_schema import GenericResponse
from typing import List
from sqlalchemy import select
from datetime import datetime, timezone

study_task_controller = Blueprint("task_controller", __name__, url_prefix="/tasks")

@study_task_controller.get("/")
@jwt_required()
@api.validate(
    resp=Response(HTTP_200=List[StudyTaskResponse]),
    tags=["tasks"]
)
def get_tasks():
    user_id = current_user.id

    subject_id = request.args.get("subject_id", type=int)
    completed = request.args.get("completed")

    query = StudyTask.query.join(Subject).filter(Subject.user_id == user_id)

    if subject_id:
        query = query.filter(StudyTask.subject_id == subject_id)

    if completed is not None:
        completed = completed.lower() == "true"
        query = query.filter(StudyTask.completed == completed)

    tasks = query.order_by(StudyTask.due_date.asc()).all()

    return [StudyTaskResponse.model_validate(task) for task in tasks], 200

@study_task_controller.post("/")
@jwt_required()
@api.validate(
    json=StudyTaskRequest,
    resp=Response(
        HTTP_201=StudyTaskResponse, 
        HTTP_400=GenericResponse),
    tags=["tasks"]
)
def create_task():
    data = request.json

    subject = db.session.scalars(
    select(Subject).filter_by(
        id=data["subject_id"],
        user_id=current_user.id
    )
    ).first()

    if subject is None:
        return {"msg": "Subject not found."}, 404
    
    task = StudyTask(
        
        title = data["title"],
        description = data["description"],
        due_date = data["due_date"],
        subject_id=subject.id
    )
    
    db.session.add(task)
    db.session.commit()

    return StudyTaskResponse.model_validate(task).to_response_dict(), 201 

@study_task_controller.get("/<int:id>")
@jwt_required()
@api.validate(
    resp=Response(HTTP_200=StudyTaskResponse,
    HTTP_404=GenericResponse),
    tags=["tasks"]
)
def get_taks(id):
    task = db.session.scalars(
        select(StudyTask).join(Subject).filter(StudyTask.id == id, Subject.user_id == current_user.id,)
    ).first()

    if task is None:
        return {"msg": "Task not found."}, 404

    return StudyTaskResponse.model_validate(task).to_response_dict(), 200

@study_task_controller.put("/<int:id>")
@jwt_required()
@api.validate(
    json=StudyTaskUpdateRequest,
    resp=Response(
        HTTP_200=StudyTaskResponse,
        HTTP_404=GenericResponse,
    ),
    tags=["tasks"],
)
def update_task(id):
    data = request.json

    task = db.session.scalars(
        select(StudyTask)
        .join(Subject)
        .filter(
            StudyTask.id == id,
            Subject.user_id == current_user.id,
        )
    ).first()

    if task is None:
        return {"msg": "Task not found."}, 404

    subject = db.session.scalars(
        select(Subject).filter_by(
            id=data["subject_id"],
            user_id=current_user.id,
        )
    ).first()

    if subject is None:
        return {"msg": "Subject not found."}, 404

    task.title = data["title"]
    task.description = data["description"]
    task.due_date = data["due_date"]
    task.subject_id = subject.id

    if data["completed"] and not task.completed:
        task.completed_at = datetime.now(timezone.utc)
    elif not data["completed"]:
        task.completed_at = None

    task.completed = data["completed"]

    db.session.commit()

    return StudyTaskResponse.model_validate(task).to_response_dict(), 200

@study_task_controller.delete("/<int:id>")
@jwt_required()
@api.validate(
    resp=Response(
        HTTP_200=GenericResponse,
        HTTP_404=GenericResponse,
    ),
    tags=["tasks"],
)
def delete_task(id):
    task = db.session.scalars(
        select(StudyTask)
        .join(Subject)
        .filter(
            StudyTask.id == id,
            Subject.user_id == current_user.id,
        )
    ).first()

    if task is None:
        return {"msg": "Task not found."}, 404

    db.session.delete(task)
    db.session.commit()

    return {"msg": "Task deleted successfully."}, 200
