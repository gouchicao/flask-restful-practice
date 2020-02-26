import os
import requests
import json


API_URL = 'http://127.0.0.1:5000/'
MAX_RETRIES = 60


def post_body_form_data():
    json_data = {
        "name": "wjj",
        "age": 40
    }
    json_str = json.dumps(json_data)
    response = requests.post(API_URL + "test/post_body_form_data", data={'i': 123, 'str': 'hello world', 'json_str': json_str})
    print(response.status_code, response.reason)


def post_body_form_json():
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(API_URL + "test/post_body_form_json", headers=headers, data='{"name": "wjj", "age": 40, "sons": ["wrj", "wxl"]}')
    print(response.status_code, response.reason)


def post_body_form_file():
    filename = 'test.jpg'
    files = {'file': (filename, open(filename, 'rb'), 'application/octet-stream', {})}
    response = requests.post(API_URL + "test/post_body_form_file", files=files)
    print(response.status_code, response.reason)


if __name__ == '__main__':
    post_body_form_data()
    post_body_form_json()
    post_body_form_file()
