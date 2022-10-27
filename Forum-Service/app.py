from flask import Flask, Blueprint, jsonify
from flask_restplus import Api
from ma import ma
from db import db

from resources.forum import Forum, ForumList, forum_ns, forums_ns
from resources.comment import Comment, CommentList, comment_ns, comments_ns
from resources.reply import Reply, ReplyList, reply_ns, replies_ns
from marshmallow import ValidationError

app = Flask(__name__)
bluePrint = Blueprint('api', __name__, url_prefix='/api')
api = Api(bluePrint, doc='/doc', title='Forum Service')
app.register_blueprint(bluePrint)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

api.add_namespace(comment_ns)
api.add_namespace(comments_ns)
api.add_namespace(forum_ns)
api.add_namespace(forums_ns)
api.add_namespace(reply_ns)
api.add_namespace(replies_ns)


@app.before_first_request
def create_tables():
    db.create_all()


@api.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify(error.messages), 400

reply_ns.add_resource(Reply, '/<int:id>')
replies_ns.add_resource(ReplyList, "")
comment_ns.add_resource(Comment, '/<int:id>')
comments_ns.add_resource(CommentList, "")
forum_ns.add_resource(Forum, '/<int:id>')
forums_ns.add_resource(ForumList, "")

if __name__ == '__main__':
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5001, debug=True,host='0.0.0.0')
