from flask import request
from flask_restplus import Resource, fields, Namespace

from models.forum import ForumModel
from schemas.forum import ForumSchema

FORUM_NOT_FOUND = "Forum not found."
FORUM_ALREADY_EXISTS = "Forum '{}' Already exists."

forum_ns = Namespace('forum', description='Forum related operations')
forums_ns = Namespace('forums', description='Forums related operations')

forum_schema = ForumSchema()
forum_list_schema = ForumSchema(many=True)

# Model required by flask_restplus for expect
forum = forums_ns.model('Forum', {
    'track_id': fields.Integer,
    'forum_name': fields.String('Forum Name')
})


class Forum(Resource):
    def get(self, id):
        forum_data = ForumModel.find_by_id(id)
        if forum_data:
            return forum_schema.dump(forum_data)
        return {'message': FORUM_NOT_FOUND}, 404

    def delete(self, id):
        forum_data = ForumModel.find_by_id(id)
        if forum_data:
            forum_data.delete_from_db()
            return {'message': "Forum Deleted successfully"}, 200
        return {'message': FORUM_NOT_FOUND}, 404

    @forum_ns.expect(forum)
    def put(self, id):
        forum_data = ForumModel.find_by_id(id)
        forum_json = request.get_json()

        if forum_data:
            forum_data.track_id = forum_json['track_id']
            forum_data.forum_name = forum_json['forum_name']
        else:
            forum_data = forum_schema.load(forum_json)

        forum_data.save_to_db()
        return forum_schema.dump(forum_data), 200


class ForumList(Resource):
    @forums_ns.doc('Get all the Forums')
    def get(self):
        return forum_list_schema.dump(ForumModel.find_all()), 200

    @forums_ns.expect(forum)
    @forums_ns.doc('Create a Forum')
    def post(self):
        forum_json = request.get_json()
        track_id = forum_json['track_id']
        forum_name = forum_json['forum_name']
        if ForumModel.find_by_forum_name(forum_name):
            return {'message': FORUM_ALREADY_EXISTS.format(forum_name)}, 400

        forum_data = forum_schema.load(forum_json)
        forum_data.save_to_db()

        return forum_schema.dump(forum_data), 201
