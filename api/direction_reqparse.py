from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('id', required=True, type=int)
parser.add_argument('name', required=True)
parser.add_argument('description', required=False)
