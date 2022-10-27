from flask import request
from flask_restplus import Resource, fields, Namespace

from models.reply import ReplyModel
from schemas.reply import ReplySchema

REPLY_NOT_FOUND = "Reply not found."


reply_ns = Namespace('reply', description='Reply related operations')
replies_ns = Namespace('replies', description='Replies related operations')

reply_schema = ReplySchema()
reply_list_schema = ReplySchema(many=True)

#Model required by flask_restplus for expect
reply = replies_ns.model('Reply', {
    'reply': fields.String('Reply'),
    'username': fields.String('Username'),
    'comment_id': fields.Integer
})


class Reply(Resource):

    def get(self, id):
        reply_data = ReplyModel.find_by_id(id)
        if reply_data:
            return reply_schema.dump(reply_data)
        return {'message': REPLY_NOT_FOUND}, 404

    def delete(self,id):
        reply_data = ReplyModel.find_by_id(id)
        if reply_data:
            reply_data.delete_from_db()
            return {'message': "Reply Deleted successfully"}, 200
        return {'message': REPLY_NOT_FOUND}, 404

    @reply_ns.expect(reply)
    def put(self, id):
        reply_data = ReplyModel.find_by_id(id)
        reply_json = request.get_json()

        if reply_data:
            reply_data.reply = reply_json['reply']
            reply_data.username = reply_json['username']
            reply_data.card_id = reply_json['card_id']
        else:
            reply_data = reply_schema.load(reply_json)

        reply_data.save_to_db()
        return reply_schema.dump(reply_data), 200


class ReplyList(Resource):
    @replies_ns.doc('Get all the Replies')
    def get(self):
        return reply_list_schema.dump(ReplyModel.find_all()), 200

    @replies_ns.expect(reply)
    @replies_ns.doc('Create an Reply')
    def post(self):
        reply_json = request.get_json()
        reply_data = reply_schema.load(reply_json)
        reply_data.save_to_db()

        return reply_schema.dump(reply_data), 201
