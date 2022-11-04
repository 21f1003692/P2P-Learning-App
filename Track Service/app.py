from flask import Flask, Blueprint, jsonify
from flask_restplus import Api
from ma import ma
from db import db

from resources.track import Track, TrackList, track_ns, tracks_ns
from resources.forum import Forum, ForumList, forum_ns, forums_ns
from resources.article import Article, ArticleList, article_ns, articles_ns
from resources.like import Like, LikeList, like_ns, likes_ns
from marshmallow import ValidationError

app = Flask(__name__)
bluePrint = Blueprint('api', __name__, url_prefix='/api')
api = Api(bluePrint, doc='/doc', title='Track Service')
app.register_blueprint(bluePrint)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

api.add_namespace(track_ns)
api.add_namespace(tracks_ns)
api.add_namespace(forum_ns)
api.add_namespace(forums_ns)
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

track_ns.add_resource(Track, '/<int:id>')
tracks_ns.add_resource(TrackList, "")
forum_ns.add_resource(Forum, '/<int:id>')
forums_ns.add_resource(ForumList, "")
article_ns.add_resource(Article, '/<int:id>')
articles_ns.add_resource(ArticleList, "")
like_ns.add_resource(Like, '/<int:id>')
likes_ns.add_resource(LikeList, "")

if __name__ == '__main__':
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5002, debug=True,host='0.0.0.0')
