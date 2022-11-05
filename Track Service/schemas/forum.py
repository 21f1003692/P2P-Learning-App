from ma import ma
from models.forum import ForumModel
from schemas.comment import CommentSchema
from schemas.reply import ReplySchema


class ForumSchema(ma.SQLAlchemyAutoSchema):
    comments = ma.Nested(CommentSchema, many=True)
    replies = ma.Nested(ReplySchema, many=True)

    class Meta:
        model = ForumModel
        load_instance = True
        include_fk = True
