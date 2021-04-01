# If a file named wsgi.py is present in your repository, 
# it will be used as the entry point to your application. 
# This can be overridden with the environment variable APP_MODULE.
import json
from flask import Flask, jsonify, request
from prediction import predict, predict1
import time
application = Flask(__name__)

@application.route('/')
@application.route('/status')
def status():
    return jsonify({'status': 'ok'})

# The older model
# doesn't use ship_locations
@application.route('/prediction1', methods=['POST'])
def object_detection1():
    tic = time.perf_counter()
    data = request.json
    # data = json.dumps(data)
    # body = json.loads(data)
    print(data)
    # bState = data['board_state']
    res = jsonify(predict1(data))
    toc = time.perf_counter()
    print(f"time taken {toc - tic:0.4f} seconds")
    return res


# v5
# use ship_locations
#attacks center
@application.route('/prediction2', methods=['POST'])
def object_detection2():
    tic = time.perf_counter()
    data = request.json
    # data = json.dumps(data)
    # body = json.loads(data)
    print(data)
    # bState = data['board_state']
    res = jsonify(predict1(data))
    toc = time.perf_counter()
    print(f"time taken {toc - tic:0.4f} seconds")
    return res


# v5
# use ship_locations
#attacks random center or middle side rows
@application.route('/prediction', methods=['POST'])
def object_detection():
    tic = time.perf_counter()
    data = request.json
    # data = json.dumps(data)
    # body = json.loads(data)
    print(data)
    # bState = data['board_state']
    res = jsonify(predict(data))
    toc = time.perf_counter()
    print(f"time taken {toc - tic:0.4f} seconds")
    return res