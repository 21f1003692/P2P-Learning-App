from ma import ma
from models.comment import CommentModel
from schemas.reply import ReplySchema


class CommentSchema(ma.SQLAlchemyAutoSchema):
    replies = ma.Nested(ReplySchema, many=True)

    class Meta:
        model = CommentModel
        load_instance = True
        load_only = ("forum",)
        include_fk= True