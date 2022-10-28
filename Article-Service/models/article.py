from datetime import datetime
from db import db
from typing import List


class ArticleModel(db.Model):
    __tablename__ = "article"

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, primary_key=True)
    track_id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    likes = db.relationship("LikesModel",lazy="dynamic",primaryjoin="ArticleModel.id == LikesModel.article_id")


    def __init__(self, url, user_id, track_id):
        self.url = url
        self.user_id = user_id
        self.track_id = track_id

    def __repr__(self):
        return 'AnswerModel(url=%s, user_id=%s, track_id=%s, timestamp=%s)' % (self.url, self.user_id, self.track_id, self.timestamp)

    def json(self):
        return {'url': self.url, 'user_id': self.user_id, 'track_id': self.track_id, 'timstamp': self.timestamp}

    @classmethod
    def find_by_id(cls, _id) -> "ArticleModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["ArticleModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
