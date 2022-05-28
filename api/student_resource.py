from flask import jsonify
from flask_restful import Resource, abort

from api.student_reqparse import parser
from db.models import Student
from db.database import db_session


def abort_if_student_not_found(student_id):
    student = Student.query.get(student_id)
    if not student:
        abort(404, message=f"Student {student_id} not found")


class StudentResource(Resource):
    def get(self, student_id):
        abort_if_student_not_found(student_id)
        student = Student.query.get(student_id)
        return student.to_dict()

    def delete(self, student_id):
        abort_if_student_not_found(student_id)
        student = Student.query.get(student_id)
        db_session.delete(student)
        db_session.commit()
        return jsonify({'success': 'OK'})


class StudentListResource(Resource):
    def get(self):
        students = Student.query.all()
        return jsonify({'students': [student.to_dict() for student in students]})

    def post(self):
        args = parser.parse_args()
        student = Student(**args)
        db_session.add(student)
        db_session.commit()
        return jsonify({'success': 'OK'})
