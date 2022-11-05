from flask import request
from flask_restplus import Resource, fields, Namespace

from models.comment import CommentModel
from models.reply import ReplyModel
from resources.reply import ReplyList
from schemas.comment import CommentSchema

import jsonify

COMMENT_NOT_FOUND = "Comment not found."


comment_ns = Namespace('comment', description='Comment related operations')
comments_ns = Namespace('comments', description='Comments related operations')

comment_schema = CommentSchema()
comment_list_schema = CommentSchema(many=True)

#Model required by flask_restplus for expect
comment = comments_ns.model('Comment', {
    'comment': fields.String('Comment'),
    'username': fields.String('Username'),
    'forum_id': fields.Integer
})


class Comment(Resource):

    def get(self, id):
        comment_data = CommentModel.find_by_id(id)
        if comment_data:
            return comment_schema.dump(comment_data)
        return {'message': COMMENT_NOT_FOUND}, 404

    def delete(self,id):
        comment_data = CommentModel.find_by_id(id)
        if comment_data:
            comment_data.delete_from_db()
            return {'message': "Comment Deleted successfully"}, 200
        return {'message': COMMENT_NOT_FOUND}, 404

    @comment_ns.expect(comment)
    def put(self, id):
        comment_data = CommentModel.find_by_id(id)
        comment_json = request.get_json()

        if comment_data:
            comment_data.comment = comment_json['comment']
            comment_data.username = comment_json['username']
            comment_data.forum_id = comment_json['forum_id']
        else:
            comment_data = comment_schema.load(comment_json)

        comment_data.save_to_db()
        return comment_schema.dump(comment_data), 200


class CommentList(Resource):
    @comments_ns.doc('Get all the Comments')
    def get(self):
        return (comment_list_schema.dump(CommentModel.find_all())), 200

    @comments_ns.expect(comment)
    @comments_ns.doc('Create an Comment')
    def post(self):
        comment_json = request.get_json()
        comment_data = comment_schema.load(comment_json)
        comment_data.save_to_db()

        return comment_schema.dump(comment_data), 201
