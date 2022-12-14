from datetime import datetime
from db import db
from typing import List


class AnswerModel(db.Model):
    __tablename__ = "answer"

    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(1000))
    user_id = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    question_id = db.Column(db.Integer,db.ForeignKey('question.id'),nullable=False)
    question = db.relationship("QuestionModel")

    def __init__(self, answer, user_id, question_id):
        self.answer = answer
        self.user_id = user_id
        self.question_id = question_id

    def __repr__(self):
        return 'AnswerModel(answer=%s, user_id=%s, question_id=%s, timestamp=%s)' % (self.answer, self.user_id, self.question_id, self.timestamp)

    def json(self):
        return {'answer': self.answer, 'user_id': self.user_id, 'question_id': self.question_id, 'question_id': self.timestamp}

    @classmethod
    def find_by_id(cls, _id) -> "AnswerModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["AnswerModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
