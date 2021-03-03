# If a file named wsgi.py is present in your repository, 
# it will be used as the entry point to your application. 
# This can be overridden with the environment variable APP_MODULE.
import json
from flask import Flask, jsonify, request
from prediction import predict, predict1

application = Flask(__name__)

@application.route('/')
@application.route('/status')
def status():
    return jsonify({'status': 'ok'})

# The older model
# doesn't use ship_locations
@application.route('/prediction1', methods=['POST'])
def object_detection1():
    data = request.json
    # data = json.dumps(data)
    # body = json.loads(data)
    print(data)
    # bState = data['board_state']
    return jsonify(predict1(data))

@application.route('/prediction', methods=['POST'])
def object_detection():
    data = request.json
    # data = json.dumps(data)
    # body = json.loads(data)
    print(data)
    # bState = data['board_state']
    return jsonify(predict(data))