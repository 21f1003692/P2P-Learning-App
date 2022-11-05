from db import db
from typing import List


class TrackModel(db.Model):
    __tablename__ = "track"
    id = db.Column(db.Integer, primary_key=True)
    track_name = db.Column(db.String(100))
    track_info = db.Column(db.String(1000))
    
    forums = db.relationship("ForumModel",lazy="dynamic",primaryjoin="TrackModel.id == ForumModel.track_id")
    # articles = db.relationship("ArticleModel",lazy="dynamic",primaryjoin="TrackModel.id == ArticleModel.track_id")

    def __init__(self, track_name, track_info):
        self.track_name = track_name
        self.track_info = track_info

    def __repr__(self):
        return 'TrackModel(track_name=%s, track_info=%s)' % (self.track_name, self.track_info)

    @classmethod
    def find_by_track_name(cls, track_name) -> "TrackModel":
        return cls.query.filter_by(track_name=track_name).first()

    @classmethod
    def find_by_id(cls, _id) -> "TrackModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["TrackModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
