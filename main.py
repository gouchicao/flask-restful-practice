import os
import json
import logging
import tempfile

import werkzeug
from flask import Flask, request, jsonify, make_response, redirect, url_for, send_file
from flask_restful import reqparse, abort, Api, Resource
from flask_restful_swagger import swagger


app = Flask(__name__, static_folder='static')
api = swagger.docs(Api(app), apiVersion='1.0',
                   description='Flask RESTful Test API')

file_handler = logging.FileHandler('app.log')
app.logger.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
))
app.logger.addHandler(file_handler)


class PostBodyFormData(Resource):
    """Post Body Form Data"""

    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('i', type=int, location='form', help='int data')
        parse.add_argument('str', type=str, location='form', help='string data')
        parse.add_argument('json_str', type=str, location='form', help='json string data')
        args = parse.parse_args()

        print(args)
        print('>> i ', args.i)
        print('>> str ', args.str)
        print('>> json_str ', args.json_str)
        if args.json_str:
            json_data = json.loads(args.json_str)
            print(json_data)

        return 'PostBodyFormData Succeed', 200


class PostBodyFormJson(Resource):
    """Post Body Form JSON"""

    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('name', type=str, location='json')
        parse.add_argument('age', type=int, location='json')
        parse.add_argument('sons', type=list, location='json')
        args = parse.parse_args()

        print('>> name', args.name)
        print('>> age', args.age)
        print('>> sons', args.sons)

        return 'PostBodyFormJson Succeed', 200


class PostBodyFormFile(Resource):
    """上传文件"""

    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parse.parse_args()

        file_obj = args.file
        if not file_obj:
            app.logger.info('file no setting')
            return 'file no setting', 417

        with open('out_'+file_obj.filename, 'wb+') as f:
            file_data = file_obj.read()
            f.write(file_data)

        return 'PostBodyFormFile Succeed', 200


class UploadFileAndValues(Resource):
    """上传文件和数据"""

    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        parse.add_argument('json_str', type=str, location='form')
        args = parse.parse_args()

        print('00 ', args.json_str)
        print(json.loads(args.json_str))

        file_obj = args.file
        if not file_obj:
            app.logger.info('file no setting')
            return 'file no setting', 417

        with open('out_'+file_obj.filename, 'wb+') as f:
            file_data = file_obj.read()
            f.write(file_data)

        return 'upload file and data succeed', 200


api.add_resource(PostBodyFormData, '/test/post_body_form_data')
api.add_resource(PostBodyFormJson, '/test/post_body_form_json')
api.add_resource(PostBodyFormFile, '/test/post_body_form_file')
api.add_resource(UploadFileAndValues, '/test/upload_file_and_values')


@app.route('/docs')
def docs():
  return redirect('/static/docs.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
