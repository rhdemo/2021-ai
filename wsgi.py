# If a file named wsgi.py is present in your repository, 
# it will be used as the entry point to your application. 
# This can be overridden with the environment variable APP_MODULE.
import json
from flask import Flask, jsonify, request
from prediction import predict

application = Flask(__name__)

@application.route('/')
@application.route('/status')
def status():
    return jsonify({'status': 'ok'})


@application.route('/prediction', methods=['POST'])
def object_detection():
    data = request.data or '{}'
    body = json.loads(data)
    return jsonify(predict(body))
