from db import db
from typing import List


class ForumModel(db.Model):
    __tablename__ = "forum"
    id = db.Column(db.Integer, primary_key=True)
    track_id = db.Column(db.Integer)
    forum_name = db.Column(db.String(100), index=True, unique=True)
    
    comments = db.relationship("CommentModel",lazy="dynamic",primaryjoin="ForumModel.id == CommentModel.forum_id")

    def __init__(self, track_id, forum_name):
        self.track_id = track_id
        self.forum_name = forum_name

    def __repr__(self):
        return 'ForumModel(forum_name=%s)' % self.forum_name

    @classmethod
    def find_by_forum_name(cls, forum_name) -> "ForumModel":
        return cls.query.filter_by(forum_name=forum_name).first()

    @classmethod
    def find_by_id(cls, _id) -> "ForumModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["ForumModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
