"""
docstring
"""
import json

from app import webserver
from flask import request, jsonify
# Example endpoint definition

@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    """
    docstring
    """
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json

        # Process the received data
        # For demonstration purposes, just echoing back the received data
        response = {"message": "Received data successfully", "data": data}

        # Sending back a JSON response
        return jsonify(response)
        # Method Not Allowed
    return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):

    # Check if job_id is valid
    job_string = job_id
    job_id = list(job_id.split('_'))
    job_id = int(job_id[-1])
    if job_id >= webserver.job_counter:
        webserver.logger.info("Invalid job_id")
        return jsonify({'status': 'Error', 'reason': 'Invalid job_id'})

    if job_id in webserver.tasks_runner.jobs_done:
        webserver.logger.info(f"Request job_id done, job_id_{job_id} found")

        with open(f"results/{job_string}.json", "r") as fout:
            rez = json.load(fout)
        return jsonify({'status' : 'done', 'data': rez})
    # If not, return running status
    webserver.logger.info("Request job_id done, job_id still running")
    return jsonify({'status': 'running'})

@webserver.route("/api/jobs_num", methods=['GET'])
def jobs_num():

    #webserver.logger.info("GET /api/jobs_num")
    return jsonify({'status' : 'done', 'value': webserver.tasks_runner.jobs})



@webserver.route('/api/jobs', methods=['GET'])
def jobs():

    webserver.logger.info("GET /api/jobs")
    with webserver.lock:
        a = webserver.job_counter

    rezultat = {}
    for i in range(0, a):
        if i in webserver.tasks_runner.jobs_done or i == 0:
            rezultat[f"job_id_{i}"] = 'done'
        else:
            if webserver.tasks_runner.up is True:
                rezultat[f"job_id_{i}"] = 'running'
    webserver.logger.info("GET /api/jobs done")
    return jsonify({'status' : 'done', 'data' : rezultat})

@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():

    # Get request data
    data = request.json
    webserver.logger.info("POST /api/states_mean" )
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id
    with webserver.lock:
        webserver.job_counter += 1
        webserver.tasks_runner.queue_jobs.put((0, data, webserver.job_counter - 1))
        return jsonify({'job_id' : 'job_id_' + str(webserver.job_counter - 1)})

@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():

    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id
    webserver.logger.info("POST /api/state_mean" )
    data = request.json
    with webserver.lock:
        webserver.job_counter += 1
        webserver.tasks_runner.queue_jobs.put((1, data, webserver.job_counter - 1))
        return jsonify({'job_id' : 'job_id_' + str(webserver.job_counter - 1)})


@webserver.route('/api/best5', methods=['POST'])
def best5_request():

    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id
    webserver.logger.info("POST /api/best5" )
    data = request.json
    with webserver.lock:
        webserver.job_counter += 1
        webserver.tasks_runner.queue_jobs.put((2, data, webserver.job_counter - 1))
        return jsonify({'job_id' : 'job_id_' + str(webserver.job_counter - 1)})

@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    """
    Get request data
    Register job. Don't wait for task to finish
    Increment job_id counter
    Return associated job_id
    """
    webserver.logger.info("POST /api/worst5" )
    data = request.json
    with webserver.lock:
        webserver.job_counter += 1
        webserver.tasks_runner.queue_jobs.put((3, data, webserver.job_counter - 1))
        return jsonify({'job_id' : 'job_id_' + str(webserver.job_counter - 1)})

@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    """     
    Get request data
    Register job. Don't wait for task to finish
    Increment job_id counter
    Return associated job_id
    """
    data = request.json
    webserver.logger.info(f"POST /api/global_mean, question: {data}" )
    with webserver.lock:
        webserver.job_counter += 1
        webserver.tasks_runner.queue_jobs.put((4, data, webserver.job_counter - 1))
        return jsonify({'job_id' : 'job_id_' + str(webserver.job_counter - 1)})

@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    """     Get request data
     Register job. Don't wait for task to finish
     Increment job_id counter
     Return associated job_id
    """
    webserver.logger.info("POST /api/diff_from_mean" )
    data = request.json
    with webserver.lock:
        webserver.job_counter += 1
        webserver.tasks_runner.queue_jobs.put((5, data, webserver.job_counter - 1))
        return jsonify({'job_id' : 'job_id_' + str(webserver.job_counter - 1)})


@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    """     Get request data
     Register job. Don't wait for task to finish
     Increment job_id counter
     Return associated job_id
    """
    webserver.logger.info("POST /api/state_diff_from_mean" )
    data = request.json
    with webserver.lock:
        webserver.job_counter += 1
        webserver.tasks_runner.queue_jobs.put((6, data, webserver.job_counter - 1))
        return jsonify({'job_id' : 'job_id_' + str(webserver.job_counter - 1)})

@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    """     Get request data
     Register job. Don't wait for task to finish
     Increment job_id counter
     Return associated job_id
    """
    webserver.logger.info("POST /api/mean_by_category" )
    data = request.json
    with webserver.lock:
        webserver.job_counter += 1
        webserver.tasks_runner.queue_jobs.put((7, data, webserver.job_counter - 1))
        return jsonify({'job_id' : 'job_id_' + str(webserver.job_counter - 1)})

@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    """     Get request data
     Register job. Don't wait for task to finish
     Increment job_id counter
     Return associated job_id
    """
    webserver.logger.info("POST /api/state_mean_by_category" )
    data = request.json

    with webserver.lock:
        webserver.job_counter += 1
        webserver.tasks_runner.queue_jobs.put((8, data, webserver.job_counter - 1))
        return jsonify({'job_id' : 'job_id_' + str(webserver.job_counter - 1)})

# You can check localhost in your browser to see what this displays
@webserver.route('/')
@webserver.route('/index')
def index():
    """     Get request data
     Register job. Don't wait for task to finish
     Increment job_id counter
     Return associated job_id
    """
    routes = get_defined_routes()
    msg = "Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg


@webserver.route('/api/graceful_shutdown', methods = ['GET'])
def stop():
    """     Get request data
     Register job. Don't wait for task to finish
     Increment job_id counter
     Return associated job_id
    """
    webserver.logger.info("GET /api/graceful_shutdown")
    webserver.tasks_runner.event.set()
    webserver.tasks_runner.queue_jobs.put((9, None, webserver.job_counter - 1))
    webserver.logger.info("The server can be shutdowned.")
    return jsonify({'status' : 'shutdown'})


def get_defined_routes():
    """     Get request data
     Register job. Don't wait for task to finish
     Increment job_id counter
     Return associated job_id
    """
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
