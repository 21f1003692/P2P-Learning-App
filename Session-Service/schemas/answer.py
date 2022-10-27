from ma import ma
from models.answer import AnswerModel


class AnswerSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = AnswerModel
        load_instance = True
        load_only = ("question",)
        include_fk= True