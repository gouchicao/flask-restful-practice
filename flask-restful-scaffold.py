import os
import json
import logging

import werkzeug
from flask import Flask, redirect, jsonify
from flask_restful import Api, Resource, reqparse, abort
from flask_restful_swagger import swagger


app = Flask(__name__, static_folder='static')
api = Api(app)

log_file = 'app.log'
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
))
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)


class GetData(Resource):
    def get(self):

        return jsonify({"i":123, "str":"hello world"})

class PostData(Resource):
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('i', type=int, location='form', required=True, help='int data')
        parse.add_argument('str', type=str, location='form', help='string data')
        args = parse.parse_args()

        print('>> i ', args.i)
        print('>> str ', args.str)

        return {}, 200


api.add_resource(GetData, '/get_data')
api.add_resource(PostData, '/post_data')


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
