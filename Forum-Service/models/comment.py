from datetime import datetime
from db import db
from typing import List


class CommentModel(db.Model):
    __tablename__ = "comment"

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(1000))
    username = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    forum_id =db.Column(db.Integer,db.ForeignKey('forum.id'),nullable=False)
    forum = db.relationship("ForumModel",)

    replies = db.relationship("ReplyModel",lazy="dynamic",primaryjoin="CommentModel.id == ReplyModel.comment_id")

    def __init__(self, comment, username, forum_id):
        self.comment = comment
        self.username = username
        self.forum_id = forum_id

    def __repr__(self):
        return 'CommentModel(comment=%s, username=%s, forum_id=%s, timestamp=%s)' % (self.comment, self.username, self.forum_id, self.timestamp)

    def json(self):
        return {'comment': self.comment, 'username': self.username, 'forum_id': self.forum_id, 'timestamp': self.timestamp}

    @classmethod
    def find_by_id(cls, _id) -> "CommentModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["CommentModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
