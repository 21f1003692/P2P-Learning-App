from db import db
from typing import List


class NotificationModel(db.Model):
    __tablename__ = "notification"

    id = db.Column(db.Integer, primary_key=True)
    notification_msg = db.Column(db.String(1000))
    track_id = db.Column(db.Integer,nullable=False)
    session_id = db.Column(db.Integer,nullable=False)


    def __init__(self, notification_msg, track_id, session_id):
        self.notification_msg = notification_msg
        self.track_id = track_id
        self.session_id = session_id

    def __repr__(self):
        return 'AnswerModel(notification_msg=%s, track_id=%s, session_id=%s, timestamp=%s)' % (self.notification_msg, self.track_id, self.session_id)

    def json(self):
        return {'notification_msg': self.notification_msg, 'track_id': self.track_id, 'session_id': self.session_id}

    @classmethod
    def find_by_id(cls, _id) -> "NotificationModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["NotificationModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
