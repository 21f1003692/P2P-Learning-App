from datetime import datetime
from db import db
from typing import List


class ReplyModel(db.Model):
    __tablename__ = "reply"

    id = db.Column(db.Integer, primary_key=True)
    reply = db.Column(db.String(1000))
    username = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    comment_id = db.Column(db.Integer,db.ForeignKey('comment.id'),nullable=False)
    comment = db.relationship("CommentModel")

    def __init__(self, reply, username, comment_id):
        self.reply = reply
        self.username = username
        self.comment_id = comment_id

    def __repr__(self):
        return 'ReplyModel(reply=%s, username=%s, comment_id=%s, timestamp=%s)' % (self.reply, self.username, self.comment_id, self.timestamp)

    def json(self):
        return {'reply': self.reply, 'username': self.username, 'comment_id': self.timestamp, 'comment_id': self.timestamp}

    @classmethod
    def find_by_id(cls, _id) -> "ReplyModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["ReplyModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
