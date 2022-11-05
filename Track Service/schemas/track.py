from ma import ma
from models.track import TrackModel
from schemas.forum import ForumSchema
from schemas.article import ArticleSchema


class TrackSchema(ma.SQLAlchemyAutoSchema):
    forums = ma.Nested(ForumSchema, many=True)
    articles = ma.Nested(ArticleSchema, many=True)

    class Meta:
        model = TrackModel
        load_instance = True
        include_fk = True
