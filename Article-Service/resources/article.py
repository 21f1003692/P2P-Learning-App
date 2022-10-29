from flask import request
from flask_restplus import Resource, fields, Namespace

from models.article import ArticleModel
from schemas.article import ArticleSchema

ARTICLE_NOT_FOUND = "Article not found."


article_ns = Namespace('article', description='article related operations')
articles_ns = Namespace('articles', description='articles related operations')

article_schema = ArticleSchema()
article_list_schema = ArticleSchema(many=True)

#Model required by flask_restplus for expect
article = articles_ns.model('Article', {
    'url': fields.String('Url'),
    'user_id': fields.Integer,
    'track_id': fields.Integer
})


class Article(Resource):

    def get(self, id):
        article_data = ArticleModel.find_by_id(id)
        if article_data:
            return article_schema.dump(article_data)
        return {'message': ARTICLE_NOT_FOUND}, 404

    def delete(self,id):
        article_data = ArticleModel.find_by_id(id)
        if article_data:
            article_data.delete_from_db()
            return {'message': "Question Deleted successfully"}, 200
        return {'message': ARTICLE_NOT_FOUND}, 404

    @article_ns.expect(article)
    def put(self, id):
        article_data = ArticleModel.find_by_id(id)
        article_json = request.get_json()

        if article_data:
            article_data.url = article_json['url']
            article_data.user_id = article_json['user_id']
            article_data.track_id = article_json['track_id']
        else:
            article_data = article_schema.load(article_json)

        article_data.save_to_db()
        return article_schema.dump(article_data), 200


class ArticleList(Resource):
    @articles_ns.doc('Get all the articles')
    def get(self):
        return article_list_schema.dump(ArticleModel.find_all()), 200

    @articles_ns.expect(article)
    @articles_ns.doc('Create an Article')
    def post(self):
        article_json = request.get_json()
        article_data = article_schema.load(article_json)
        article_data.save_to_db()

        return article_schema.dump(article_data), 201
