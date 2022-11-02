from ma import ma
from models.session import SessionModel
from schemas.question import QuestionSchema
from schemas.invitee import InviteeSchema
from schemas.answer import AnswerSchema


class SessionSchema(ma.SQLAlchemyAutoSchema):
    questions = ma.Nested(QuestionSchema, many=True)
    answers = ma.Nested(AnswerSchema, many=True)
    invitees = ma.Nested(InviteeSchema, many=True)

    class Meta:
        model = SessionModel
        load_instance = True
        include_fk = True
