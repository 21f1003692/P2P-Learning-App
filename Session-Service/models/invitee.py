from datetime import datetime
from db import db
from typing import List


class InviteeModel(db.Model):
    __tablename__ = "invitee"

    id = db.Column(db.Integer, primary_key=True)
    invitee_uid = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    session_id =db.Column(db.Integer,db.ForeignKey('session.id'),nullable=False)
    session = db.relationship("SessionModel",)

    def __init__(self, invitee_uid, user_id, session_id):
        self.invitee_uid = invitee_uid
        self.user_id = user_id
        self.session_id = session_id

    def __repr__(self):
        return 'InviteeModel(invitee_uid=%s, user_id=%s, session_id=%s, timestamp=%s)' % (self.invitee_uid, self.user_id, self.session_id, self.timestamp)

    def json(self):
        return {'invitee_uid': self.invitee_uid, 'user_id': self.user_id, 'session_id': self.session_id, 'timestamp': self.timestamp}

    @classmethod
    def find_by_id(cls, _id) -> "InviteeModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["InviteeModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
