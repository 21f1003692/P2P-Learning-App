from ma import ma
from models.invitee import InviteeModel


class InviteeSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = InviteeModel
        load_instance = True
        load_only = ("session",)
        include_fk= True