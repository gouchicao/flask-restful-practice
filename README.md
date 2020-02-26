# Flask RESTful 实践

## [REST服务脚手架](flask-restful-scaffold.py)
``` Python
import os
import logging

from flask import Flask, redirect, jsonify
from flask_restful import Api, Resource, reqparse


app = Flask(__name__, static_folder='static')
api = Api(app)

log_file = 'app.log'
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
))
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)


# curl --request GET 'http://127.0.0.1:5000/get_data'
class GetData(Resource):
    def get(self):

        return jsonify({"i":123, "str":"hello world"})


# curl --request POST 'http://127.0.0.1:5000/post_data' --form 'i=123' --form 'str=hello world'
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
```

## POST data
### 服务端
``` python
class PostBodyFormData(Resource):
    """Post Body Form Data"""

    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('i', type=int, location='form', required=True, help='int data')
        parse.add_argument('str', type=str, location='form', help='string data')
        parse.add_argument('list', type=str, location='form', help='list data')
        parse.add_argument('json_str', type=str, location='form', help='json string data')
        args = parse.parse_args()

        print('>> i ', args.i)
        print('>> str ', args.str)
        print('>> list ', args.list)
        print('>> json_str ', args.json_str)
        if args.json_str:
            json_data = json.loads(args.json_str)
            print(json_data)

        return 'PostBodyFormData Succeed', 200

api.add_resource(PostBodyFormData, '/test/post_body_form_data')
```

### 客户端
* curl
``` bash
curl --location --request POST 'http://127.0.0.1:5000/test/post_body_form_data' \
--header 'Content-Type: multipart/form-data' \
--form 'i=123' \
--form 'str=hello world' \
--form 'list=[1, 2, 3]' \
--form 'json_str={"name": "wjj", "age": 40}'
```

* Python
``` python
json_data = {
    "name": "wjj",
    "age": 40
}
json_str = json.dumps(json_data)

data = {
    'i': 123, 
    'str': 'hello world', 
    'list': '[1, 2, 3]', 
    'json_str': json_str}
response = requests.post(API_URL + "test/post_body_form_data", data=data)
print(response.status_code, response.reason, response.text, end='')
```

## POST JSON
### 服务端
``` python
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

api.add_resource(PostBodyFormJson, '/test/post_body_form_json')
```

### 客户端
* curl
``` bash
curl --location --request POST 'http://127.0.0.1:5000/test/post_body_form_json' \
--header 'Content-Type: application/json' \
--data-raw '{"name": "wjj", "age": 40, "sons": ["wrj", "wxl"]}'
```

* Python
``` python
headers = {
    'Content-Type': 'application/json'
}

json_data = {
    "name": "wjj",
    "age": 40,
    "sons": ["wrj", "wxl"]
}
json_str = json.dumps(json_data)

response = requests.post(API_URL + "test/post_body_form_json", headers=headers, data=json_str)
print(response.status_code, response.reason, response.text, end='')
```

## POST File
### 服务端
``` python
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

        with open('tmp/out_'+file_obj.filename, 'wb+') as f:
            file_data = file_obj.read()
            f.write(file_data)

        return 'PostBodyFormFile Succeed', 200

api.add_resource(PostBodyFormFile, '/test/post_body_form_file')
```

### 客户端
* curl
``` bash
curl --location --request POST 'http://127.0.0.1:5000/test/post_body_form_file' \
--header 'Content-Type: application/octet-stream' \
--form 'file=@test.jpg'
```

* Python
``` python
filename = 'test.jpg'
files = {'file': (filename, open(filename, 'rb'), 'application/octet-stream', {})}
response = requests.post(API_URL + "test/post_body_form_file", files=files)
print(response.status_code, response.reason, response.text, end='')
```
