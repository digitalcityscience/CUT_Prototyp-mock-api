from http import HTTPStatus

from flask import Flask, request, abort, make_response, jsonify
from flask_compress import Compress
from flask_cors import CORS

from celery.result import AsyncResult
from celery_app import app as celery_app

import tasks

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
Compress(app)


@app.route('/')
@app.errorhandler(404)
def not_found(message: str):
    return make_response(
        jsonify({'error': message}),
        404
    )


@app.errorhandler(401)
def not_found(message: str):
    return make_response(
        jsonify({'error': message}),
        404
    )


@app.errorhandler(400)
def bad_request(message: str):
    return make_response(
        jsonify({'error': message}),
        400
    )


# process calculation requests 
@app.route("/cut-public-api/noise/processes/traffic-noise/execution", methods=['POST'])
def process_task_noise():
    # Validate request
    if not request.json:
        abort(400)

    # Validate request
    if not request.json.get('buildings'):
        abort(400, "Missing buildings in request body")
    if not request.json.get('roads'):
        abort(400, "Missing roads in request body")
    if not request.json.get('traffic_quota'):
        abort(400, "Missing traffic_quota in request body")
    if not request.json.get('max_speed'):
        abort(400, "Missing max_speed in calculation_settings")

    try:
        task = tasks.compute_task_noise.delay(request.json)
        response = {'job_id': task.id}

        # return jsonify(response), HTTPStatus.OK
        return make_response(
            jsonify(response),
            HTTPStatus.OK,
        )
    except KeyError as e:
        print("THIS IS THE ERROR %s " % e)
        print("THIS IS THE request %s " % request)

        return make_response(
            jsonify(e),
            HTTPStatus.OK,
        )
    
# process calculation requests 
@app.route("/cut-public-api/wind/processes/wind-comfort/execution", methods=['POST'])
def process_task_wind():
    # Validate request
    if not request.json:
        abort(400)

    # Validate request
    if not request.json.get('buildings'):
        abort(400, "Missing buildings in request body")
    if not request.json.get('calculation_settings'):
        abort(400, "Missing calculation_settings in request body")
    if not request.json.get('calculation_settings').get('wind_speed'):
        abort(400, "Missing wind speed in calculation_settings")

    try:
        # trigger async task. result object will contain task id etc. 
        task = tasks.compute_task_wind.delay(request.json)
        response = {'job_id': task.id}

        # return jsonify(response), HTTPStatus.OK
        return make_response(
            jsonify(response),
            HTTPStatus.OK,
        )
    except KeyError as e:
        print("THIS IS THE ERROR %s " % e)
        print("THIS IS THE request %s " % request)

        return make_response(
            jsonify(e),
            HTTPStatus.OK,
        )
    

"""
    *PENDING*
        The task is waiting for execution.
    *STARTED*
        The task has been started.
    *RETRY*
        The task is to be retried, possibly because of failure.
    *FAILURE*
        The task raised an exception, or has exceeded the retry limit.
        The :attr:`result` attribute then contains the
        exception raised by the task.
    *SUCCESS*
        The task executed successfully.  The :attr:`result` attribute
        then contains the tasks return value.
"""

@app.route("/cut-public-api/noise/jobs/<taskId>/status", methods=['GET'])
def is_task_ready_noise(task_id: str):
    async_result = AsyncResult(task_id, app=celery_app)

    state = async_result.state
    if state == 'FAILURE':
        state = 'FAILURE : ' + str(async_result.get())

    response = {
        "status": state
    }

    return make_response(
        response,
        HTTPStatus.OK,
    )

@app.route("/cut-public-api/wind/jobs/<taskId>/status", methods=['GET'])
def is_task_ready_wind(task_id: str):
    async_result = AsyncResult(task_id, app=celery_app)

    state = async_result.state
    if state == 'FAILURE':
        state = 'FAILURE : ' + str(async_result.get())

    response = {
        "status": state
    }

    return make_response(
        response,
        HTTPStatus.OK,
    )



@app.route("/cut-public-api/noise/jobs/<taskId>", methods=['GET'])
def get_task_noise(task_id: str):
    async_result = AsyncResult(task_id, app=celery_app)

    # Fields available
    # https://docs.celeryproject.org/en/stable/reference/celery.result.html#celery.result.Result
    response = {
        'taskId': async_result.id,
        'taskState': async_result.state,
    }
    if async_result.ready():
        response['result'] = async_result.get()

    return make_response(
        response,
        HTTPStatus.OK,
    )

@app.route("/cut-public-api/wind/jobs/<taskId>", methods=['GET'])
def get_task_wind(task_id: str):
    async_result = AsyncResult(task_id, app=celery_app)

    # Fields available
    # https://docs.celeryproject.org/en/stable/reference/celery.result.html#celery.result.Result
    response = {
        'taskId': async_result.id,
        'taskState': async_result.state,
    }
    if async_result.ready():
        response['result'] = async_result.get()

    return make_response(
        response,
        HTTPStatus.OK,
    )
