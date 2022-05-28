from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('id', required=True, type=int)
parser.add_argument('user_id', required=True, type=int)
parser.add_argument('educational_institution')
parser.add_argument('edu_class')
parser.add_argument('health')
parser.add_argument('parent_id', type=int)
parser.add_argument('temp_password')
