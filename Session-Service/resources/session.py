from flask import request
from flask_restplus import Resource, fields, Namespace

from models.session import SessionModel
from schemas.session import SessionSchema

SESSION_NOT_FOUND = "Session not found."
SESSION_ALREADY_EXISTS = "Session '{}' Already exists."

session_ns = Namespace('session', description='Session related operations')
sessions_ns = Namespace('sessions', description='Sessions related operations')

session_schema = SessionSchema()
session_list_schema = SessionSchema(many=True)

# Model required by flask_restplus for expect
session = sessions_ns.model('Session', {
    'track_id': fields.Integer,
    'session_name': fields.String('Session Name'),
    'session_description': fields.String('Session Description'),
    'session_url': fields.String('Session URL'),
    'begin_time': fields.DateTime,
    'end_time': fields.DateTime
})


class Session(Resource):
    def get(self, id):
        session_data = SessionModel.find_by_id(id)
        if session_data:
            return session_schema.dump(session_data)
        return {'message': SESSION_NOT_FOUND}, 404

    def delete(self, id):
        session_data = SessionModel.find_by_id(id)
        if session_data:
            session_data.delete_from_db()
            return {'message': "Session Deleted successfully"}, 200
        return {'message': SESSION_NOT_FOUND}, 404

    @session_ns.expect(session)
    def put(self, id):
        session_data = SessionModel.find_by_id(id)
        session_json = request.get_json()

        if session_data:
            session_data.track_id = session_json['track_id']
            session_data.session_name = session_json['session_name']
            session_data.session_description = session_json['session_description']
            session_data.session_url = session_json['session_url']
            session_data.begin_time = session_json['begin_time']
            session_data.end_time = session_json['end_time']
        else:
            session_data = session_schema.load(session_json)

        session_data.save_to_db()
        return session_schema.dump(session_data), 200


class SessionList(Resource):
    @sessions_ns.doc('Get all the Sessions')
    def get(self):
        return session_list_schema.dump(SessionModel.find_all()), 200

    @sessions_ns.expect(session)
    @sessions_ns.doc('Create a Session')
    def post(self):
        session_json = request.get_json()
        session_name = session_json['session_name']
        # if SessionModel.find_by_session_name(session_name):
        #     return {'message': SESSION_ALREADY_EXISTS.format(session_name)}, 400

        session_data = session_schema.load(session_json)
        session_data.save_to_db()

        return session_schema.dump(session_data), 201
