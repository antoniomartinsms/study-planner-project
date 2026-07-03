from factory import db
from pydantic import BaseModel, ConfigDict
from utils.response_schema import OrmBase, ResponseBase, GenericResponse
from datetime import datetime, timezone

class StudyTask(db.Model):
    __tablename__ = "study_task"

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column (db.String(64), nullable = False, index = True)
    description = db.Column(db.String (400))
    due_date = db.Column(db.DateTime, nullable = False)
    completed = db.Column(db.Boolean, default = False)
    completed_at = db.Column(db.DateTime)
    subject_id = db.Column(db.Integer, db.ForeignKey("subject.id"), nullable= False)

    subject = db.relationship("Subject", back_populates="tasks")

class StudyTaskResponse(OrmBase):
    id: int
    title: str
    description: str
    due_date: datetime | None
    completed: bool
    completed_at: datetime | None
    subject_id: int

class StudyTaskRequest(ResponseBase):
    title: str
    description: str | None = None
    due_date: datetime
    subject_id: int

class StudyTaskUpdateRequest(ResponseBase):
    title: str
    description: str | None = None
    due_date: datetime
    subject_id: int
    completed: bool