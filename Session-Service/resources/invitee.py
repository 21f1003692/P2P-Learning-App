from flask import request
from flask_restplus import Resource, fields, Namespace

from models.invitee import InviteeModel
from schemas.invitee import InviteeSchema

INVITEE_NOT_FOUND = "Invitee not found."


invitee_ns = Namespace('invitee', description='Invitee related operations')
invitees_ns = Namespace('invitees', description='Invitees related operations')

invitee_schema = InviteeSchema()
invitee_list_schema = InviteeSchema(many=True)

#Model required by flask_restplus for expect
invitee = invitees_ns.model('Invitee', {
    'session_id': fields.Integer, 
    'invitee_uid': fields.Integer,
    'user_id': fields.Integer
})


class Invitee(Resource):

    def get(self, id):
        invitee_data = InviteeModel.find_by_id(id)
        if invitee_data:
            return invitee_schema.dump(invitee_data)
        return {'message': INVITEE_NOT_FOUND}, 404

    def delete(self,id):
        invitee_data = InviteeModel.find_by_id(id)
        if invitee_data:
            invitee_data.delete_from_db()
            return {'message': "Invitee Deleted successfully"}, 200
        return {'message': INVITEE_NOT_FOUND}, 404

    @invitee_ns.expect(invitee)
    def put(self, id):
        invitee_data = InviteeModel.find_by_id(id)
        invitee_json = request.get_json()

        if invitee_data:
            invitee_data.invitee_uid = invitee_json['invitee_uid']
            invitee_data.user_id = invitee_json['user_id']
            invitee_data.session_id = invitee_json['session_id']
        else:
            invitee_data = invitee_schema.load(invitee_json)

        invitee_data.save_to_db()
        return invitee_schema.dump(invitee_data), 200


class InviteeList(Resource):
    @invitees_ns.doc('Get all the Invitees')
    def get(self):
        return invitee_list_schema.dump(InviteeModel.find_all()), 200

    @invitees_ns.expect(invitee)
    @invitees_ns.doc('Create an Invitee')
    def post(self):
        invitee_json = request.get_json()
        invitee_data = invitee_schema.load(invitee_json)
        invitee_data.save_to_db()

        return invitee_schema.dump(invitee_data), 201
