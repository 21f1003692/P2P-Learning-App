from flask import Flask, Blueprint, jsonify
from flask_restplus import Api
from ma import ma
from db import db

from resources.session import Session, SessionList, session_ns, sessions_ns
from resources.question import Question, QuestionList, question_ns, questions_ns
from resources.answer import Answer, AnswerList, answer_ns, answers_ns
from marshmallow import ValidationError

app = Flask(__name__)
bluePrint = Blueprint('api', __name__, url_prefix='/api')
api = Api(bluePrint, doc='/doc', title='Session Service')
app.register_blueprint(bluePrint)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

api.add_namespace(question_ns)
api.add_namespace(questions_ns)
api.add_namespace(session_ns)
api.add_namespace(sessions_ns)
api.add_namespace(answer_ns)
api.add_namespace(answers_ns)


@app.before_first_request
def create_tables():
    db.create_all()


@api.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify(error.messages), 400

answer_ns.add_resource(Answer, '/<int:id>')
answers_ns.add_resource(AnswerList, "")
question_ns.add_resource(Question, '/<int:id>')
questions_ns.add_resource(QuestionList, "")
session_ns.add_resource(Session, '/<int:id>')
sessions_ns.add_resource(SessionList, "")

if __name__ == '__main__':
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5002, debug=True,host='0.0.0.0')
