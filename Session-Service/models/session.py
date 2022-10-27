from db import db
from typing import List


class SessionModel(db.Model):
    __tablename__ = "session"
    id = db.Column(db.Integer, primary_key=True)
    track_id = db.Column(db.Integer)
    session_name = db.Column(db.String(100))
    session_description = db.Column(db.String(1000))
    session_url = db.Column(db.String(1000))
    begin_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    
    questions = db.relationship("QuestionModel",lazy="dynamic",primaryjoin="SessionModel.id == QuestionModel.session_id")

    def __init__(self, track_id, session_name, session_description, session_url, begin_time, end_time):
        self.track_id = track_id
        self.session_name = session_name
        self.session_description = session_description
        self.session_url = session_url
        self.begin_time = begin_time
        self.end_time = end_time

    def __repr__(self):
        return 'SessionModel(track_id=%s, session_name=%s, session_description=%s, session_url=%s, begin_time=%s,  end_time=%s)' % (self.track_id, self.session_name, self.session_description, self.session_url, self.begin_time, self.end_time)

    @classmethod
    def find_by_session_name(cls, session_name) -> "SessionModel":
        return cls.query.filter_by(session_name=session_name).first()

    @classmethod
    def find_by_id(cls, _id) -> "SessionModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["SessionModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
