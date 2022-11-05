from ma import ma
from models.like import LikeModel


class LikeSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = LikeModel
        load_instance = True
        load_only = ("article",)
        include_fk= True