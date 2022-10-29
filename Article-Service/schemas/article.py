from ma import ma
from models.article import ArticleModel
from schemas.like import LikeSchema


class ArticleSchema(ma.SQLAlchemyAutoSchema):
    answers = ma.Nested(LikeSchema, many=True)

    class Meta:
        model = ArticleModel
        load_instance = True
        include_fk= True