from ma import ma
from models.question import QuestionModel
from schemas.answer import AnswerSchema


class QuestionSchema(ma.SQLAlchemyAutoSchema):
    answers = ma.Nested(AnswerSchema, many=True)

    class Meta:
        model = QuestionModel
        load_instance = True
        load_only = ("session",)
        include_fk= True