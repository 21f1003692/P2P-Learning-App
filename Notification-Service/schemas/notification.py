from ma import ma
from models.notification import NotificationModel


class NotificationSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = NotificationModel
        load_instance = True
        include_fk= True