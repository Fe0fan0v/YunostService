from flask import jsonify
from flask_restful import Resource, abort

from api.direction_reqparse import parser
from db.models import Direction
from db.database import db_session


def abort_if_direction_not_found(direction_id):
    direction = Direction.query.get(direction_id)
    if not direction:
        abort(404, message=f"Direction {direction_id} not found")


class DirectionResource(Resource):
    def get(self, direction_id):
        abort_if_direction_not_found(direction_id)
        direction = Direction.query.get(direction_id)
        return jsonify({'direction': direction.to_dict()})

    def delete(self, direction_id):
        abort_if_direction_not_found(direction_id)
        direction = Direction.query.get(direction_id)
        db_session.delete(direction)
        db_session.commit()
        return jsonify({'success': 'OK'})


class DirectionListResource(Resource):
    def get(self):
        directions = Direction.query.all()
        return jsonify({'directions': [direction.to_dict() for direction in directions]})

    def post(self):
        args = parser.parse_args()
        direction = Direction(**args)
        db_session.add(direction)
        db_session.commit()
        return jsonify({'success': 'OK'})
