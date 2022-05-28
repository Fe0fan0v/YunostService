from flask import jsonify
from flask_restful import Resource, abort

from api.area_reqparse import parser
from db.models import Area
from db.database import db_session


def abort_if_area_not_found(area_id):
    area = Area.query.get(area_id)
    if not area:
        abort(404, message=f"Area {area_id} not found")


class AreaResource(Resource):
    def get(self, area_id):
        abort_if_area_not_found(area_id)
        area = Area.query.get(area_id)
        return jsonify({'area': area.to_dict()})

    def delete(self, area_id):
        abort_if_area_not_found(area_id)
        area = Area.query.get(area_id)
        db_session.delete(area)
        db_session.commit()
        return jsonify({'success': 'OK'})


class AreaListResource(Resource):
    def get(self):
        areas = Area.query.all()
        return jsonify({'areas': [area.to_dict() for area in areas]})

    def post(self):
        args = parser.parse_args()
        area = Area(**args)
        db_session.add(area)
        db_session.commit()
        return jsonify({'success': 'OK'})
