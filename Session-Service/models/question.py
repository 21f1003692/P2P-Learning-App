from datetime import datetime
from db import db
from typing import List


class QuestionModel(db.Model):
    __tablename__ = "question"

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(1000))
    username = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    session_id =db.Column(db.Integer,db.ForeignKey('session.id'),nullable=False)
    session = db.relationship("SessionModel",)

    answers = db.relationship("AnswerModel",lazy="dynamic",primaryjoin="QuestionModel.id == AnswerModel.question_id")

    def __init__(self, question, username, session_id):
        self.question = question
        self.username = username
        self.session_id = session_id

    def __repr__(self):
        return 'QuestionModel(question=%s, username=%s, session_id=%s, timestamp=%s)' % (self.question, self.username, self.session_id, self.timestamp)

    def json(self):
        return {'question': self.question, 'username': self.username, 'session_id': self.session_id, 'timestamp': self.timestamp}

    @classmethod
    def find_by_id(cls, _id) -> "QuestionModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["QuestionModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
