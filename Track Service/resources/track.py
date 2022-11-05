from flask import request
from flask_restplus import Resource, fields, Namespace

from models.track import TrackModel
from schemas.track import TrackSchema

TRACK_NOT_FOUND = "Track not found."
TRACK_ALREADY_EXISTS = "Track '{}' Already exists."

track_ns = Namespace('track', description='Track related operations')
tracks_ns = Namespace('tracks', description='Tracks related operations')

track_schema = TrackSchema()
track_list_schema = TrackSchema(many=True)

# Model required by flask_restplus for expect
track = tracks_ns.model('Track', {
    'track_name': fields.String('Track Name'),
    'track_info' : fields.String('Track Info')

})


class Track(Resource):
    def get(self, id):
        track_data = TrackModel.find_by_id(id)
        if track_data:
            return track_schema.dump(track_data)
        return {'message': TRACK_NOT_FOUND}, 404

    def delete(self, id):
        track_data = TrackModel.find_by_id(id)
        if track_data:
            track_data.delete_from_db()
            return {'message': "Track Deleted successfully"}, 200
        return {'message': TRACK_NOT_FOUND}, 404

    @track_ns.expect(track)
    def put(self, id):
        track_data = TrackModel.find_by_id(id)
        track_json = request.get_json()

        if track_data:
            track_data.track_name = track_json['track_name']
            track_data.track_info = track_json['track_info']
            
        else:
            track_data = track_schema.load(track_json)

        track_data.save_to_db()
        return track_schema.dump(track_data), 200


class TrackList(Resource):
    @tracks_ns.doc('Get all the Tracks')
    def get(self):
        return track_list_schema.dump(TrackModel.find_all()), 200

    @tracks_ns.expect(track)
    @tracks_ns.doc('Create a Track')
    def post(self):
        track_json = request.get_json()
        track_name = track_json['track_name']
        if TrackModel.find_by_track_name(track_name):
            return {'message': TRACK_ALREADY_EXISTS.format(track_name)}, 400

        track_data = track_schema.load(track_json)
        track_data.save_to_db()

        return track_schema.dump(track_data), 201
