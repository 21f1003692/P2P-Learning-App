from flask import request
from flask_restplus import Resource, fields, Namespace

from models.like import LikeModel
from schemas.like import LikeSchema

LIKES_NOT_FOUND = "no likes"


like_ns = Namespace('like', description='Like related operations')
likes_ns = Namespace('likes', description='Likes related operations')

like_schema = LikeSchema()
like__list_schema = LikeSchema(many=True)

#Model required by flask_restplus for expect
like = likes_ns.model('Like', {
    'article_id': fields.Integer,
    'user_id': fields.Integer
})


class Like(Resource):

    def get(self, id):
        like_data = LikeModel.find_by_id(id)
        if like_data:
            return like_schema.dump(like_data)
        return {'message': LIKES_NOT_FOUND}, 404

    def delete(self,id):
        like_data = LikeModel.find_by_id(id)
        if like_data:
            like_data.delete_from_db()
            return {'message': "Like Deleted successfully"}, 200
        return {'message': LIKES_NOT_FOUND}, 404

    @like_ns.expect(like)
    def put(self, id):
        like_data = LikeModel.find_by_id(id)
        like_json = request.get_json()

        if like_data:
            like_data.user_id = like_json['user_id']
            like_data.article_id = like_json['article_id']
        else:
            like_data = like_schema.load(like_json)

        like_data.save_to_db()
        return like_schema.dump(like_data), 200


class LikeList(Resource):
    @likes_ns.doc('Get all the Likes')
    def get(self):
        return like__list_schema.dump(LikeModel.find_all()), 200

    @likes_ns.expect(like)
    @likes_ns.doc('Create an Like')
    def post(self):
        like_json = request.get_json()
        like_data = like_schema.load(like_json)
        like_data.save_to_db()

        return like_schema.dump(like_data), 201
