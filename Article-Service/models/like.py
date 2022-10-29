from datetime import datetime
from db import db
from typing import List


class LikeModel(db.Model):
    __tablename__ = "like"

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    article_id = db.Column(db.Integer,db.ForeignKey('article.id'),nullable=False)
    article = db.relationship("ArticleModel")

    user_id = db.Column(db.Integer,nullable=False)


    def __init__(self, article_id, user_id):
        self.article_id = article_id
        self.user_id = user_id

    def __repr__(self):
        return 'LikesModel(article_id=%s, user_id=%s, timestamp=%s)' % (self.article_id, self.user_id, self.timestamp)

    def json(self):
        return {'article_id': self.article_id, 'user_id': self.user_id, 'timestamp': self.timestamp}

    @classmethod
    def find_by_id(cls, _id) -> "LikeModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["LikeModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
