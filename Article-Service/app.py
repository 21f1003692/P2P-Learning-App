from flask import Flask, Blueprint, jsonify
from flask_restplus import Api
from ma import ma
from db import db

from resources.article import Article, ArticleList, article_ns, articles_ns
from resources.like import Like, LikeList, like_ns, likes_ns
from marshmallow import ValidationError

app = Flask(__name__)
bluePrint = Blueprint('api', __name__, url_prefix='/api')
api = Api(bluePrint, doc='/doc', title='Article Service')
app.register_blueprint(bluePrint)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

api.add_namespace(article_ns)
api.add_namespace(articles_ns)
api.add_namespace(like_ns)
api.add_namespace(likes_ns)


@app.before_first_request
def create_tables():
    db.create_all()


@api.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify(error.messages), 400

like_ns.add_resource(Like, '/<int:id>')
likes_ns.add_resource(LikeList, "")
article_ns.add_resource(Article, '/<int:id>')
articles_ns.add_resource(ArticleList, "")


if __name__ == '__main__':
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5003, debug=True,host='0.0.0.0')
