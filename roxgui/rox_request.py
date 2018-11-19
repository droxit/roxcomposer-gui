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
from roxgui.settings import SERVICE_DIR, SESSION_DIR, ROX_CONNECTOR_IP

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
FORBIDDEN_SERVICES = ['basic_reporting']

# Store metadata for current GUI session.
current_session = None

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


def get_running_service_names() -> RoxResponse:
    """
    Get names of all currently running services ignoring those specified in FORBIDDEN_SERVICES.
    :returns: RoxResponse instance containing a name list of all currently running services.
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
        # Extract service names.
        running_service_names = list(r.json().keys())
        # Exclude services specified in forbidden services list.
        running_service_names = [name for name in running_service_names if name not in FORBIDDEN_SERVICES]
        res = RoxResponse(True)
        res.data = running_service_names
        return res


def create_service(ip: str, port: int, name: str, class_path: str, output_file_path: str = "") -> RoxResponse:
    """
    Create new service with given metadata and store it as JSON file in services folder.
    :param ip: IP address of service.
    :param port: Used port number.
    :param name: Service name.
    :param class_path: Classpath of service implementation.
    :param output_file_path: Path to output file (default: "").
    :return: RoxResponse instance documenting if service could be created.
    """
    # Use service name as JSON file name.
    file_name = name + ".json"
    # Store JSON file to service folder.
    file_path = os.path.join(SERVICE_DIR, file_name)
    # Create JSON dictionary.
    json_dict = {
        "classpath": class_path,
        "params": {
            "ip": ip,
            "port": port,
            "name": name
        }
    }
    if output_file_path:
        json_dict["params"]["filepath"] = output_file_path
    # Write specified dictionary to JSON file.
    try:
        with open(file_path, 'w') as fd:
            json.dump(json_dict, fd)
    except OSError as err:
        error_msg = _create_file_error(file_path, str(err))
        return RoxResponse(False, error_msg)
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


def remove_pipeline() -> RoxResponse:
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
        return RoxResponse(True, result_msg)


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


def watch_services(service_names, rox_session=None, timeout=SESSION_TIMEOUT) -> RoxResponse:
    """
    Add specified services to given sessions watchlist.
    :param service_names: List of service names which should be watched.
    :param rox_session: A dictionary with an ID, a timeout and a set of services which are currently watched.
    :param timeout: Timeout (in seconds) after which given services are no longer watched.
    :return: RoxResponse instance documenting if services could be added to watchlist.
    """

    url = create_rox_connector_url("log_observer")

    if rox_session is None:
        # There is no session yet, so start a new one.

        rox_session = dict()
        rox_session['services'] = set()
        rox_session['timeout'] = timeout

        content = {'lines': 100, 'timeout': timeout, 'services': service_names}

        try:
            r = requests.put(url, headers=JSON_HEADER, json=content)
        except requests.exceptions.ConnectionError as err:
            error_msg = _create_connection_error(str(err))
            return RoxResponse(False, error_msg)

        if r.status_code != 200:
            error_msg = _create_http_status_error(r.status_code, r.text)
            return RoxResponse(False, error_msg)

        rox_session['id'] = r.json()['sessionid']

        for s in service_names:
            rox_session['services'].add(s)

        res = RoxResponse(True, r.text)
        res.data = rox_session
        return res
    else:
        # Session already exist, so update it.

        unwatched_services = list(rox_session['services'] - set(service_names))

        if unwatched_services:
            # There are sessions which should be added to watchlist.

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

            for s in response['ok']:
                rox_session['services'].add(s)

            res = RoxResponse(True, r.text)
            res.data = rox_session
            return res
        else:
            # All specified services are already watched.
            return RoxResponse(False, "All services are already watched.")


def unwatch_services() -> RoxResponse:
    return RoxResponse(False, "Not implemented yet.")


def get_service_logs(session=None):
    if session is None:
        error_msg = "Trying to get logs, but no session instantiated."
        return RoxResponse(False, error_msg)

    url = create_rox_connector_url("log_observer")
    content = {'sessionid': session['id']}

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
