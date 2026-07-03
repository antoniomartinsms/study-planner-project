from factory import api, db
from spectree import Response
from flask import request, Blueprint
from flask_jwt_extended import jwt_required, current_user

from models.subject import (
    Subject,
    SubjectResponse,
    SubjectRequest,
    SubjectUpdateRequest,
)

from models.study_task import StudyTask

from utils.response_schema import GenericResponse

from sqlalchemy import select
from typing import List

subject_controller = Blueprint(
    "subject_controller",
    __name__,
    url_prefix="/subjects"
)


def subject_to_response(subject: Subject):
    total_tasks = len(subject.tasks)

    completed_tasks = 0

    for task in subject.tasks:

        if task.completed:

            completed_tasks += 1

    progress = (
        (completed_tasks / total_tasks) * 100
        if total_tasks > 0
        else 0
    )

    pending_tasks = [
        task for task in subject.tasks if not task.completed
    ]

    next_due_date = None

    def pegar_data(task):
        return task.due_date

    if pending_tasks:
        next_due_date = min(
            pending_tasks,
            key=pegar_data
        ).due_date

    return SubjectResponse(
        id=subject.id,
        name=subject.name,
        description=subject.description,
        user_id=subject.user_id,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        progress_percentage=progress,
        next_due_date=next_due_date,
    )


@subject_controller.get("/")
@jwt_required()
@api.validate(
    resp=Response(
        HTTP_200=List[SubjectResponse]
    ),
    tags=["subjects"],
)
def get_subjects():

    subjects = db.session.scalars(
        select(Subject).filter_by(
            user_id=current_user.id
        )
    ).all()

    return [
        subject_to_response(subject)
        for subject in subjects
    ], 200


@subject_controller.post("/")
@jwt_required()
@api.validate(
    json=SubjectRequest,
    resp=Response(
        HTTP_201=SubjectResponse,
        HTTP_400=GenericResponse,
    ),
    tags=["subjects"],
)
def create_subject():
    """
    Create Subjects
    """
    data = request.json

    subject = Subject(
        name=data["name"],
        description=data["description"],
        user_id=current_user.id,
    )

    db.session.add(subject)
    db.session.commit()

    return subject_to_response(subject).to_response_dict(), 201


@subject_controller.get("/<int:id>")
@jwt_required()
@api.validate(
    resp=Response(
        HTTP_200=SubjectResponse,
        HTTP_404=GenericResponse,
    ),
    tags=["subjects"],
)
def get_subject(id):

    subject = db.session.scalars(
        select(Subject).filter_by(
            id=id,
            user_id=current_user.id,
        )
    ).first()

    if subject is None:
        return {"msg": "Subject not found."}, 404

    return subject_to_response(subject).to_response_dict(), 200


@subject_controller.put("/<int:id>")
@jwt_required()
@api.validate(
    json=SubjectUpdateRequest,
    resp=Response(
        HTTP_200=SubjectResponse,
        HTTP_404=GenericResponse,
    ),
    tags=["subjects"],
)
def update_subject(id):

    data = request.json

    subject = db.session.scalars(
        select(Subject).filter_by(
            id=id,
            user_id=current_user.id,
        )
    ).first()

    if subject is None:
        return {"msg": "Subject not found."}, 404

    subject.name = data["name"]
    subject.description = data["description"]

    db.session.commit()

    return subject_to_response(subject).to_response_dict(), 200


@subject_controller.delete("/<int:id>")
@jwt_required()
@api.validate(
    resp=Response(
        HTTP_200=GenericResponse,
        HTTP_404=GenericResponse,
    ),
    tags=["subjects"],
)
def delete_subject(id):

    subject = db.session.scalars(
        select(Subject).filter_by(
            id=id,
            user_id=current_user.id,
        )
    ).first()

    if subject is None:
        return {"msg": "Subject not found."}, 404

    db.session.delete(subject)
    db.session.commit()

    return {"msg": "Subject deleted successfully."}, 200