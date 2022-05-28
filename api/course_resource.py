from flask import jsonify
from flask_restful import Resource, abort

from api.course_reqparse import parser
from db.models import Course
from db.database import db_session


def abort_if_course_not_found(course_id):
    course = Course.query.get(course_id)
    if not course:
        abort(404, message=f"Course {course_id} not found")


class CourseResource(Resource):
    def get(self, course_id):
        abort_if_course_not_found(course_id)
        course = Course.query.get(course_id)
        return jsonify({'course': course.to_dict()})

    def delete(self, course_id):
        abort_if_course_not_found(course_id)
        course = Course.query.get(course_id)
        db_session.delete(course)
        db_session.commit()
        return jsonify({'success': 'OK'})


class CourseListResource(Resource):
    def get(self):
        courses = Course.query.all()
        return jsonify({'courses': [course.to_dict() for course in courses]})

    def post(self):
        args = parser.parse_args()
        course = Course(**args)
        db_session.add(course)
        db_session.commit()
        return jsonify({'success': 'OK'})
