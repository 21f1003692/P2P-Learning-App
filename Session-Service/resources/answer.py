from flask import request
from flask_restplus import Resource, fields, Namespace

from models.answer import AnswerModel
from schemas.answer import AnswerSchema

ANSWER_NOT_FOUND = "Answer not found."


answer_ns = Namespace('answer', description='Answer related operations')
answers_ns = Namespace('answers', description='Answers related operations')

answer_schema = AnswerSchema()
answer_list_schema = AnswerSchema(many=True)

#Model required by flask_restplus for expect
answer = answers_ns.model('Answer', {
    'answer': fields.String('Answer'),
    'username': fields.String('Username'),
    'question_id': fields.Integer
})


class Answer(Resource):

    def get(self, id):
        answer_data = AnswerModel.find_by_id(id)
        if answer_data:
            return answer_schema.dump(answer_data)
        return {'message': ANSWER_NOT_FOUND}, 404

    def delete(self,id):
        answer_data = AnswerModel.find_by_id(id)
        if answer_data:
            answer_data.delete_from_db()
            return {'message': "Answer Deleted successfully"}, 200
        return {'message': ANSWER_NOT_FOUND}, 404

    @answer_ns.expect(answer)
    def put(self, id):
        answer_data = AnswerModel.find_by_id(id)
        answer_json = request.get_json()

        if answer_data:
            answer_data.answer = answer_json['answer']
            answer_data.username = answer_json['username']
            answer_data.card_id = answer_json['card_id']
        else:
            answer_data = answer_schema.load(answer_json)

        answer_data.save_to_db()
        return answer_schema.dump(answer_data), 200


class AnswerList(Resource):
    @answers_ns.doc('Get all the Answers')
    def get(self):
        return answer_list_schema.dump(AnswerModel.find_all()), 200

    @answers_ns.expect(answer)
    @answers_ns.doc('Create an Answer')
    def post(self):
        answer_json = request.get_json()
        answer_data = answer_schema.load(answer_json)
        answer_data.save_to_db()

        return answer_schema.dump(answer_data), 201
