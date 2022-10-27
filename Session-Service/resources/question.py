from flask import request
from flask_restplus import Resource, fields, Namespace

from models.question import QuestionModel
from models.answer import AnswerModel
from resources.answer import AnswerList
from schemas.question import QuestionSchema

QUESTION_NOT_FOUND = "Question not found."


question_ns = Namespace('question', description='Question related operations')
questions_ns = Namespace('questions', description='Questions related operations')

question_schema = QuestionSchema()
question_list_schema = QuestionSchema(many=True)

#Model required by flask_restplus for expect
question = questions_ns.model('Question', {
    'question': fields.String('Question'),
    'username': fields.String('Username'),
    'forum_id': fields.Integer
})


class Question(Resource):

    def get(self, id):
        question_data = QuestionModel.find_by_id(id)
        if question_data:
            return question_schema.dump(question_data)
        return {'message': QUESTION_NOT_FOUND}, 404

    def delete(self,id):
        question_data = QuestionModel.find_by_id(id)
        if question_data:
            question_data.delete_from_db()
            return {'message': "Question Deleted successfully"}, 200
        return {'message': QUESTION_NOT_FOUND}, 404

    @question_ns.expect(question)
    def put(self, id):
        question_data = QuestionModel.find_by_id(id)
        question_json = request.get_json()

        if question_data:
            question_data.question = question_json['question']
            question_data.username = question_json['username']
            question_data.forum_id = question_json['forum_id']
        else:
            question_data = question_schema.load(question_json)

        question_data.save_to_db()
        return question_schema.dump(question_data), 200


class QuestionList(Resource):
    @questions_ns.doc('Get all the Questions')
    def get(self):
        return question_list_schema.dump(QuestionModel.find_all()), 200

    @questions_ns.expect(question)
    @questions_ns.doc('Create an Question')
    def post(self):
        question_json = request.get_json()
        question_data = question_schema.load(question_json)
        question_data.save_to_db()

        return question_schema.dump(question_data), 201
