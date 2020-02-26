import os
import requests
import json


"""
curl
-H, --header <header/@file>
              (HTTP) Extra header to include in the request when sending HTTP to a server. You may specify any number of extra headers. Note that if you should add a custom header that has the  same
              name  as  one of the internal ones curl would use, your externally set header will be used instead of the internal one. This allows you to make even trickier stuff than curl would nor‐
              mally do. You should not replace internally set headers without knowing perfectly well what you're doing. Remove an internal header by giving a replacement without content on the right
              side  of the colon, as in: -H "Host:". If you send the custom header with no-value then its header must be terminated with a semicolon, such as -H "X-Custom-Header;" to send "X-Custom-
              Header:".
-o, --output <file>
              Write output to <file> instead of stdout. If you are using {} or [] to fetch multiple documents, you can use '#' followed by a number in the <file> specifier.  That  variable  will  be
              replaced with the current string for the URL being fetched. Like in:
--data-raw <data>
              (HTTP) This posts data similarly to -d, --data but without the special interpretation of the @ character.
-F, --form <name=content>
              (HTTP SMTP IMAP) For HTTP protocol family, this lets curl emulate a filled-in form in which a user has pressed the submit button. This causes curl to POST data using  the  Content-Type
              multipart/form-data according to RFC 2388.
-X, --request <command>
              (HTTP) Specifies a custom request method to use when communicating with the HTTP server.  The specified request method will be used instead of the method otherwise used (which defaults
              to GET). Read the HTTP 1.1 specification for details and explanations. Common additional HTTP requests include PUT and DELETE, but related technologies  like  WebDAV  offers  PROPFIND,
              COPY, MOVE and more.
-v, --verbose
              Makes  curl verbose during the operation. Useful for debugging and seeing what's going on "under the hood". A line starting with '>' means "header data" sent by curl, '<' means "header
              data" received by curl that is hidden in normal cases, and a line starting with '*' means additional info provided by curl.
-L, --location
              (HTTP)  If the server reports that the requested page has moved to a different location (indicated with a Location: header and a 3XX response code), this option will make curl redo the
              request on the new place. If used together with -i, --include or -I, --head, headers from all requested pages will be shown. When authentication is used, curl only  sends  its  creden‐
              tials  to  the  initial  host. If a redirect takes curl to a different host, it won't be able to intercept the user+password. See also --location-trusted on how to change this. You can
              limit the amount of redirects to follow by using the --max-redirs option.
"""


API_URL = 'http://127.0.0.1:5000/'
MAX_RETRIES = 60


def post_body_form_data():
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


def post_body_form_json():
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


def post_body_form_file():
    filename = 'test.jpg'
    files = {'file': (filename, open(filename, 'rb'), 'application/octet-stream', {})}
    response = requests.post(API_URL + "test/post_body_form_file", files=files)
    print(response.status_code, response.reason, response.text, end='')


if __name__ == '__main__':
    post_body_form_data()
    post_body_form_json()
    post_body_form_file()
