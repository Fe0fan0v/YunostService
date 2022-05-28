from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('id', required=True, type=int)
parser.add_argument('name', required=True)
parser.add_argument('direction_id', type=int)
parser.add_argument('area_id', type=int)
parser.add_argument('age_from', type=int)
parser.add_argument('age_to', type=int)
parser.add_argument('description')
