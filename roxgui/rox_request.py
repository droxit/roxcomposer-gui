# encoding: utf-8
#
# Communication with ROXconnector.
#
# devs@droxit.de
#
# Copyright (c) 2018 droxIT GmbH
#

import json
import logging
import os

import requests

from rox_response import RoxResponse
from roxgui.settings import SERVICE_DIR, SESSION_DIR, ROX_COMPOSER_LOG_FILE, ROX_CONNECTOR_IP

# Logging.
# ========
logging.basicConfig(filename="test.log", filemode='w', level=logging.DEBUG)

# Constants.
# ==========

# Header for JSON data.
JSON_HEADER = {"Content-Type": "application/json"}

# Error message for connection error.
MSG_CONNECTION_ERROR = "No connection to server."

# Error message for invalid services.
MSG_INVALID_SERVICE_ERROR = "Service invalid."

# Error message for missing services.
MSG_MISSING_SERVICES_ERROR = "No services specified."

# Session timeout.
SESSION_TIMEOUT = 3600

# Default services.
FORBIDDEN_SERVICES = {'basic_reporting'}

# Store names of all pipelines removed via GUI.
# TODO: Workaround because ROXcomposer does not yet support deletion of existing pipelines.
removed_pipes = []


# Error messages.
# ===============

def _create_connection_error(message: str) -> str:
    """
    Create default message concerning connection errors.
    :param message: Received error message.
    :return: Default error message concerning connection errors.
    """
    return "{}.\n{}.".format(MSG_CONNECTION_ERROR, message)


def _create_http_status_error(http_status_code: int, message: str) -> str:
    """
    Create default message concerning non-200 HTTP status codes.
    :param http_status_code: Received HTTP status code.
    :param message: Received error message.
    :return: Default error message concerning non-200 HTTP status codes.
    """
    return "Error code {}.\n{}.".format(http_status_code, message)


def _create_file_error(file_path: str, message: str):
    """
    Create default message concerning file IO errors.
    :param file_path: Corresponding file path.
    :param message: Received error message.
    :return: Default error message concerning file IO errors.
    """
    return "Unable to open file {}.\n{}.".format(file_path, message)


# ROXconnector URL.
# =================

def create_rox_connector_url(relative_path: str = "") -> str:
    """
    Create valid ROXconnector URL to specified path.
    :param relative_path: Relative URL path, i.e. everything without scheme, host and port (default: "")
    :return: Corresponding ROXconnector URL.
    """
    if not relative_path:
        # Relative path is empty.
        return "http://{}".format(ROX_CONNECTOR_IP)
    elif relative_path.endswith('/'):
        # Relative path ends with slash.
        relative_path = relative_path[:-1]
        return "http://{}/{}".format(ROX_CONNECTOR_IP, relative_path)
    else:
        return "http://{}/{}".format(ROX_CONNECTOR_IP, relative_path)


# Requests to ROXconnector.
# =========================

def get_message_history(message_id: str) -> RoxResponse:
    """
    Get history of specified message ID.
    :param message_id: Message ID.
    :return: RoxResponse instance with corresponding message history (if available).
    """
    if not message_id:
        return RoxResponse(False, "No message ID provided.")

    content = {'message_id': message_id}
    url = create_rox_connector_url("get_msg_history")

    try:
        r = requests.post(url, data=json.dumps(content), headers=JSON_HEADER)
    except requests.exceptions.ConnectionError as err:
        error_msg = _create_connection_error(str(err))
        return RoxResponse(False, error_msg)

    if r.status_code != 200:
        error_msg = _create_http_status_error(r.status_code, r.text)
        return RoxResponse(False, error_msg)
    else:
        history = r.json()
        res = RoxResponse(True)
        res.data = history
        return res


def get_running_service_jsons() -> RoxResponse:
    """
    Get JSON data of all currently running services ignoring those specified in FORBIDDEN_SERVICES.
    :return: RoxResponse instance containing a list of all currently running services.
    """

    url = create_rox_connector_url("services")

    try:
        r = requests.get(url)
    except requests.exceptions.ConnectionError as err:
        error_msg = _create_connection_error(str(err))
        return RoxResponse(False, error_msg)

    if r.status_code != 200:
        error_msg = _create_http_status_error(r.status_code, r.text)
        return RoxResponse(False, error_msg)
    else:
        res = RoxResponse(True)
        res.data = dict((key, value) for (key, value) in r.json().items() if key not in FORBIDDEN_SERVICES)
        return res


def create_service(ip: str,
                   port: int,
                   name: str,
                   class_path: str,
                   optional_param_keys: list,
                   optional_param_values: list) -> RoxResponse:
    """
    Create new service with given parameter and store it as JSON file in service folder.
    :param ip: IP address.
    :param port: Port number.
    :param name: Service name.
    :param class_path: Classpath of service implementation.
    :param optional_param_keys: List of optional parameter keys (default: []).
    :param optional_param_values: List of optional parameter values (default: []).
    :return: RoxResponse instance documenting if service could be created.
    """
    # Mandatory parameters.
    # =====================

    # Use service name as JSON file name.
    file_name = name + ".json"
    # Store JSON file in service folder.
    file_path = os.path.join(SERVICE_DIR, file_name)

    # Check if given service already exists.
    if os.path.exists(file_path):
        error_msg = "Service {} already exists.".format(name)
        return RoxResponse(False, error_msg)

    # Check if given IP is valid.
    ip_parts = ip.split('.')
    for part in ip_parts:
        part = int(part)
        if not (0 <= part <= 255):
            error_msg = "Invalid IP address: {}.".format(ip)
            return RoxResponse(False, error_msg)

    # Create JSON with mandatory parameters.
    json_dict = {
        "classpath": class_path,
        "params": {
            "ip": ip,
            "port": port,
            "name": name
        }
    }

    # Optional parameters.
    # ====================

    # Add optional parameters ignoring missing or invalid ones.
    optional_params_warning = False
    for i in range(len(optional_param_keys)):
        key = optional_param_keys[i]
        value = optional_param_values[i]
        if key and value:
            # Key and value of current parameter is not empty.
            json_dict["params"][key] = value
        else:
            # Key or value of current parameter is empty.
            optional_params_warning = True

    # Write specified dictionary to JSON file.
    try:
        with open(file_path, 'w') as fd:
            json.dump(json_dict, fd)
    except OSError as err:
        error_msg = _create_file_error(file_path, str(err))
        return RoxResponse(False, error_msg)

    # Return RoxResponse instance with corresponding warnings.
    if optional_params_warning:
        warning_msg = "Skipped invalid optional parameters."
        return RoxResponse(True, warning_msg)
    else:
        return RoxResponse(True)


def start_service(service_json: dict) -> RoxResponse:
    """
    Start service defined by given JSON dictionary.
    :param service_json: JSON dictionary defining single service.
    :return: RoxResponse instance documenting if service could be started.
    """
    if not service_json:
        # JSON data is empty and therefore invalid.
        return RoxResponse(False, MSG_INVALID_SERVICE_ERROR)

    url = create_rox_connector_url("start_service")

    try:
        r = requests.post(url, json=service_json, headers=JSON_HEADER)
    except requests.exceptions.ConnectionError as err:
        error_msg = _create_connection_error(str(err))
        return RoxResponse(False, error_msg)

    if r.status_code != 200:
        error_msg = _create_http_status_error(r.status_code, r.text)
        return RoxResponse(False, error_msg)
    else:
        return RoxResponse(True, r.text)


def start_services(service_json_list: list) -> RoxResponse:
    """
    Start all services defined by given list of JSON dictionaries.
    :param service_json_list: List of JSON dictionaries defining multiple services.
    :return: RoxResponse instance documenting which services could not be started.
    """
    if len(service_json_list) < 1:
        # Service list is empty and therefore invalid.
        return RoxResponse(False, MSG_MISSING_SERVICES_ERROR)

    # Collect names of all services which could not be started.
    not_started_json_list = []
    all_services_started = True
    for service_json in service_json_list:
        res = start_service(service_json)
        if not res.success:
            not_started_json_list.append(service_json["params"]["name"])
            all_services_started = False

    res = RoxResponse(all_services_started)
    res.error_data = not_started_json_list
    return res


def shutdown_service(service_name: dict) -> RoxResponse:
    """
    Stop service defined by given name.
    :param service_name: Service name.
    :return: RoxResponse instance documenting if service could be stopped.
    """
    if not service_name:
        # Service name is empty and therefore invalid.
        return RoxResponse(False, MSG_INVALID_SERVICE_ERROR)

    url = create_rox_connector_url("shutdown_service")
    content = {'name': service_name}

    try:
        r = requests.post(url, json=content, headers=JSON_HEADER)
    except requests.exceptions.ConnectionError as err:
        error_msg = _create_connection_error(str(err))
        return RoxResponse(False, error_msg)

    if r.status_code != 200:
        error_msg = _create_http_status_error(r.status_code, r.text)
        return RoxResponse(False, error_msg)
    else:
        return RoxResponse(True, r.text)


def shutdown_services(service_name_list: list) -> RoxResponse:
    """
    Stop all services defined by given list of service names.
    :param service_name_list: List of service names.
    :return: RoxResponse instance documenting which services could not be stopped.
    """
    if len(service_name_list) < 1:
        # Service list is empty and therefore invalid.
        return RoxResponse(False, MSG_MISSING_SERVICES_ERROR)

    # Collect names of all services which could not be stopped.
    not_stopped_name_list = []
    all_services_stopped = True
    for service_name in service_name_list:
        res = shutdown_service(service_name)
        if not res.success:
            not_stopped_name_list.append(service_name)
            all_services_stopped = False
    res = RoxResponse(all_services_stopped)
    res.error_data = not_stopped_name_list
    return res


def create_pipeline(pipe_name: str, service_names: list) -> RoxResponse:
    """
    Create new pipeline with specified services in exactly the given order.
    :param pipe_name: Name of pipeline.
    :param service_names: A list of service names. The services
    are applied in the same order as they appear in this list.
    :returns: RoxResponse instance documenting if pipeline could be created.
    """

    url = create_rox_connector_url("set_pipeline")
    content = {'name': pipe_name, 'services': service_names}

    try:
        r = requests.post(url, data=json.dumps(content), headers=JSON_HEADER)
    except requests.exceptions.ConnectionError as err:
        error_msg = _create_connection_error(str(err))
        return RoxResponse(False, error_msg)

    if r.status_code != 200:
        error_msg = _create_http_status_error(r.status_code, r.text)
        return RoxResponse(False, error_msg)
    else:
        running_service_names = list(r.json().keys())
        running_service_names = [x for x in running_service_names if x not in FORBIDDEN_SERVICES]
        res = RoxResponse(True)
        res.data = running_service_names
        return res


def remove_pipeline() -> RoxResponse: #TODO after functionality has been implemented in ROXcomposer
    raise NotImplementedError


def post_to_pipeline(pipeline_name: str, message: str) -> RoxResponse:
    """
    Post message to specified pipeline.
    :param pipeline_name: Pipeline name to which a message should be sent.
    :param message: Message as string.
    :return: RoxResponse instance documenting if data could be posted to pipeline.
    """

    url = create_rox_connector_url("post_to_pipeline")
    content = {'name': pipeline_name, 'data': message}

    try:
        r = requests.post(url, data=json.dumps(content), headers=JSON_HEADER)
    except requests.exceptions.ConnectionError as err:
        error_msg = _create_connection_error(str(err))
        return RoxResponse(False, error_msg)

    if r.status_code != 200:
        error_msg = _create_http_status_error(r.status_code, r.text)
        return RoxResponse(False, error_msg)
    else:
        result_msg = "Message {} posted: {}.".format(r.json()['message_id'], message)
        res = RoxResponse(True, result_msg)
        res.data = r.json()['message_id']
        return res


def get_pipelines() -> RoxResponse:
    """
    Get metadata of each available pipeline, i.e. pipeline name, involved services and current status.
    :returns: RoxResponse instance containing pipeline metadata.
    """

    url = create_rox_connector_url("pipelines")

    try:
        r = requests.get(url)
    except requests.exceptions.ConnectionError as err:
        error_msg = _create_connection_error(str(err))
        return RoxResponse(True, error_msg)

    if r.status_code != 200:
        error_msg = _create_http_status_error(r.status_code, r.text)
        return RoxResponse(False, error_msg)
    else:
        res = RoxResponse(True)
        res.data = r.json()
        return res


def save_session(file_name: str) -> RoxResponse:
    """
    Save current session to specified file.
    :param file_path: File name.
    :return: RoxResponse instance documenting if session could be saved.
    """
    file_path = os.path.join(SESSION_DIR, file_name)
    fd = None
    try:
        fd = open(file_path, 'w')
    except OSError as err:
        error_msg = _create_file_error(file_path, str(err))
        return RoxResponse(False, error_msg)

    url = create_rox_connector_url("dump_services_and_pipelines")

    try:
        r = requests.get(url)
    except requests.exceptions.ConnectionError as err:
        error_msg = _create_connection_error(str(err))
        return RoxResponse(False, error_msg)

    if r.status_code == 200:
        o = r.json()
        try:
            json.dump(o, fd)
        except Exception as err:
            error_msg = _create_file_error(file_path, str(err))
            return RoxResponse(False, error_msg)
        finally:
            fd.close()
        return RoxResponse(True, "Wrote session to file {}.\n{}.".format(file_path, r.text))
    else:
        fd.close()
        error_msg = _create_http_status_error(r.status_code, r.text)
        return RoxResponse(False, error_msg)


def load_session(file_name: str) -> RoxResponse:
    """
    Load session from specified JSON file.
    :param file_name: File name.
    :return: RoxResponse instance documenting if session could be loaded.
    """
    session_file = os.path.join(SESSION_DIR, file_name)
    if os.path.isfile(session_file):
        fd = open(session_file, 'r')
        restore_json = json.loads(fd.read())
        fd.close()
    else:
        error_msg = _create_file_error(session_file, "Not a valid file.")
        return RoxResponse(False, error_msg)

    url = create_rox_connector_url("load_services_and_pipelines")

    try:
        r = requests.post(url, data=json.dumps(restore_json), headers=JSON_HEADER)
    except requests.exceptions.ConnectionError as err:
        error_msg = _create_connection_error(str(err))
        return RoxResponse(False, error_msg)

    if r.status_code != 200:
        error_msg = _create_http_status_error(r.status_code, r.text)
        return RoxResponse(False, error_msg)
    else:
        return RoxResponse(True, r.text)


def watch_services(service_names: list, rox_session: dict = None, timeout: int = SESSION_TIMEOUT) -> RoxResponse:
    """
    Add specified services to given sessions watchlist.
    :param service_names: List of service names which should be watched.
    :param rox_session: A dictionary with an ID, a timeout and a set of services which are currently watched.
    :param timeout: Timeout (in seconds) after which given services are no longer watched.
    :return: RoxResponse instance documenting if services could be added to watchlist.
    """

    url = create_rox_connector_url("log_observer")

    if rox_session is None:
        return create_new_sess(service_names, timeout)
    else:
        # Session already exists, so update it.
        unwatched_services = list(set(service_names) - set(rox_session['services']))

        if unwatched_services:
            # There are services which should be added to watchlist.
            content = {'sessionid': rox_session['id'], 'services': unwatched_services}

            try:
                r = requests.post(url, headers=JSON_HEADER, json=content)
            except requests.exceptions.ConnectionError as err:
                error_msg = _create_connection_error(str(err))
                res = RoxResponse(False, error_msg)
                res.data = rox_session
                return res

            if r.status_code != 200:
                error_msg = _create_http_status_error(r.status_code, r.text)
                res = RoxResponse(False, error_msg)
                res.data = rox_session
                return res

            response = r.json()
            rox_session['services'] = set(rox_session['services'])
            for s in response['ok']:
                rox_session['services'].add(s)  # add the services that could be watched to the session dictionary
            rox_session['services'] = list(rox_session['services'])

            res = RoxResponse(True, r.text)
            res.data = rox_session
            return res  # return the session dictionary
        else:
            # All specified services are already watched.
            return RoxResponse(False, "All services are already watched.")


def create_new_sess(services: list, timeout: int = SESSION_TIMEOUT) -> RoxResponse:
    """
    Attempt to start a new log session on the ROXcomposer
    :param services: list of services that should be watched
    :param timeout: time after which session expires
    :return: response with data = session dictionary ('id', 'timeout', 'services')
    """
    # There is no session yet, so start a new one.
    rox_session = dict()
    rox_session['services'] = set()
    rox_session['timeout'] = timeout

    content = {'lines': 100, 'timeout': timeout, 'services': services}
    url = create_rox_connector_url("log_observer")

    try:
        r = requests.put(url, headers=JSON_HEADER, json=content)
    except requests.exceptions.ConnectionError as err:
        error_msg = _create_connection_error(str(err))
        res = RoxResponse(False, error_msg)
        res.data = None
        return res

    if r.status_code != 200:
        error_msg = _create_http_status_error(r.status_code, r.text)
        res = RoxResponse(False, error_msg)
        res.data = None
        return res

    # request successful, create a session dictionary
    rox_session['id'] = r.json()['sessionid']

    for s in r.json()['ok']:
        rox_session['services'].add(s)

    rox_session['services'] = list(rox_session['services'])  # convert to list

    res = RoxResponse(True, r.text)
    res.data = rox_session
    return res


def unwatch_services(service_names: list, rox_session: dict) -> RoxResponse:
    """
    The specified services are removed from the watchlist and logs concerning these services
    will no longer be sent from the server.
    :param service_names: a list of service names of services that should no longer be watched
    :param rox_session: the
    :return:
    """
    if len(service_names) < 1:
        return RoxResponse(False, "No services specified.")

    if rox_session is None:
        return RoxResponse(False, "No session specified.")

    s = list(filter(lambda service: service in rox_session['services'], service_names))

    if len(s) == 0:
        return RoxResponse(False, "The specified services are not being watched.")

    data = {'sessionid': rox_session['id'], 'services': s}
    try:
        r = requests.delete(create_rox_connector_url('log_observer'), headers=JSON_HEADER, json=data)
    except requests.exceptions.ConnectionError as err:
        error_msg = _create_connection_error(str(err))
        return RoxResponse(False, error_msg)

    if r.status_code != 200:
        error_msg = _create_http_status_error(r.status_code, r.text)
        return RoxResponse(False, error_msg)
    else:
        rox_session['services'] = list(set(rox_session['services']).difference(set(s)))
        res = RoxResponse(True, "Services no longer watched: {}.".format(s))
        res.data = rox_session
        return res


def get_service_logs(rox_session: dict):
    """

    :param rox_session:
    :return:
    """
    if rox_session is None:
        error_msg = "Trying to get logs, but no session instantiated."
        return RoxResponse(False, error_msg)

    url = create_rox_connector_url("log_observer")
    content = {'sessionid': rox_session['id']}

    try:
        r = requests.get(url, headers=JSON_HEADER, json=content)
    except requests.exceptions.ConnectionError as err:
        error_msg = _create_connection_error(str(err))
        return RoxResponse(False, error_msg)

    if r.status_code != 200:
        error_msg = _create_http_status_error(r.status_code, r.text)
        return RoxResponse(False, error_msg)

    logs = [json.loads(logline) for logline in r.json()['loglines']]
    res = RoxResponse(True, r.text)
    res.data = logs
    return res


def watch_pipelines():  # TODO
    pass


def unwatch_pipelines():  # TODO
    pass


def watch_all():  # TODO
    pass


def reset_watchers():  # TODO
    pass


def save_pipeline(file_name):  # TODO
    pass


def get_message_status(last_time=None) -> RoxResponse:
    """
    Get the last message status logs from trace log
    :param last_time: the time (in seconds) that the trace was polled from last time
    :return: RoxResponse that with data = log lines in a list
    """
    logs = []
    logfile = ROX_COMPOSER_LOG_FILE
    try:
        for line in open(logfile, "r"):
            if last_time is None:
                logs.append(line)
            else:
                line_time = json.loads(line)['time']
                # add new log lines only if they are newer than the last time logs were updated
                if line_time > last_time:
                    logs.append(line)
    except:
        return RoxResponse(False, "Could not open trace file.")

    res = RoxResponse(True, "Message trace read.")
    res.data = logs
    return res


def load_and_start_pipeline(pipe_path):
    url = create_rox_connector_url("load_and_start_pipeline")
    content = {'pipe_path': pipe_path}
    r = requests.post(url, data=json.dumps(content), headers=JSON_HEADER)
    if r.status_code == 200:
        msg = r.text
        logging.info(msg)
        return RoxResponse(True, msg)
    else:
        err = 'ERROR: {} - {}'.format(r.status_code, r.text)
        return RoxResponse(False, err)
