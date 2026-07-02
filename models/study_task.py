from factory import db
from pydantic import BaseModel, ConfigDict
from utils.response_schema import OrmBase, ResponseBase, GenericResponse

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