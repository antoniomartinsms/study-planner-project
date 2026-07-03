from factory import db
from pydantic import BaseModel, ConfigDict
from utils.response_schema import OrmBase, ResponseBase, GenericResponse
from datetime import datetime

class Subject(db.Model):
    __tablename__ = "subject"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), nullable = False, index = True)
    description = db.Column(db.String(400))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)

    user = db.relationship("User", back_populates="subjects")
    tasks = db.relationship("StudyTask", back_populates="subject")

class SubjectResponse(OrmBase):
    id: int
    name: str
    description: str | None
    user_id: int

    total_tasks: int
    completed_tasks: int
    progress_percentage: float
    next_due_date: datetime | None


class SubjectRequest(ResponseBase):
    name: str
    description: str | None = None


class SubjectUpdateRequest(ResponseBase):
    name: str
    description: str | None = None