from ma import ma
from models.reply import ReplyModel


class ReplySchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = ReplyModel
        load_instance = True
        load_only = ("comment",)
        include_fk= True