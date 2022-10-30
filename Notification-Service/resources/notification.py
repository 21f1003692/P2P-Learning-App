from flask import request
from flask_restplus import Resource, fields, Namespace

from models.notification import NotificationModel
from schemas.notification import NotificationSchema

NOTIFICATION_NOT_FOUND = "Notification not found."


notification_ns = Namespace('notification', description='Notification related operations')
notifications_ns = Namespace('notifications', description='Notifications related operations')

notification_schema = NotificationSchema()
notification_list_schema = NotificationSchema(many=True)

#Model required by flask_restplus for expect
notification = notifications_ns.model('Notification', {
    'notification_msg': fields.String('Notification_msg'),
    'track_id': fields.Integer,
    'session_id': fields.Integer
})


class Notification(Resource):

    def get(self, id):
        notification_data = NotificationModel.find_by_id(id)
        if notification_data:
            return notification_schema.dump(notification_data)
        return {'message': NOTIFICATION_NOT_FOUND}, 404

    def delete(self,id):
        notification_data = NotificationModel.find_by_id(id)
        if notification_data:
            notification_data.delete_from_db()
            return {'message': "Notification Deleted successfully"}, 200
        return {'message': NOTIFICATION_NOT_FOUND}, 404

    @notification_ns.expect(notification)
    def put(self, id):
        notification_data = NotificationModel.find_by_id(id)
        notification_json = request.get_json()

        if notification_data:
            notification_data.notification_msg = notification_json['notification_msg ']
            notification_data.track_id = notification_json['track_id']
            notification_data.session_id = notification_json['session_id']
        else:
            notification_data = notification_schema.load(notification_json)

        notification_data.save_to_db()
        return notification_schema.dump(notification_data), 200


class NotificationList(Resource):
    @notifications_ns.doc('Get all the Notifications')
    def get(self):
        return notification_list_schema.dump(NotificationModel.find_all()), 200

    @notifications_ns.expect(notification)
    @notifications_ns.doc('Create a Notification')
    def post(self):
        notification_json = request.get_json()
        notification_data = notification_schema.load(notification_json)
        notification_data.save_to_db()

        return notification_schema.dump(notification_data), 201
