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

import requests

from user_settings import ROX_DIR, ROX_URL
import os

# Log settings.
logger = logging.getLogger(__name__)
logging.basicConfig(filename="test.log", filemode='w', level=logging.INFO)

# Connection details for ROXconnector.
# ====================================

# URL to ROXconnector.
rox_connector_url = ROX_URL

# Path to ROXcomposer project.
rox_composer_dir = ROX_DIR

# Constants.
# ==========

# Header for JSON data.
JSON_HEADER = {"Content-Type": "application/json"}

# Error message for connection error.
MSG_CONNECTION_ERROR = "No connection to server."

# Error message for missing services.
MSG_MISSING_SERVICES_ERROR = "No services specified."

#Timeout for a session
SESSION_TIMEOUT = 3600


class RoxResponse():

    def __init__(self, success, message):
        self.success = success
        self.msg = message
        self.data = None



def _create_connection_error(message: str) -> str:
    """
    Create standard message concerning connection errors.
    :param message: Received error message.
    :return: Error message concerning connection errors.
    """
    return "{}.\n{}.".format(MSG_CONNECTION_ERROR, message)


def _create_http_status_error(http_status_code: int, message: str) -> str:
    """
    Create standard message concerning non-200 HTTP status codes.
    :param http_status_code: Received HTTP status code.
    :param message: Received error message.
    :return: Error message concerning non-200 HTTP status codes.
    """
    return "Error code {}.\n{}.".format(http_status_code, message)


def post_to_pipeline(pipeline_name: str, message: str) -> RoxResponse:
    """
    Post message to specified pipeline.
    :param pipeline_name: Pipeline name to which a message should be sent.
    :param message: Message as string.
    :return: Result dictionary documenting if data could be posted to pipeline.
    """

    content = {'name': pipeline_name, 'data': message}
    url = "http://{}/post_to_pipeline".format(rox_connector_url)

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


def get_msg_history(message_id: str) -> RoxResponse:
    """
    Get history of specified message ID.
    :param message_id: Message ID.
    :return: Result dictionary with corresponding message history (if available).
    """

    content = {'message_id': message_id}
    url = "http://{}/get_msg_history".format(rox_connector_url)

    try:
        r = requests.post(url, data=json.dumps(content), headers=JSON_HEADER)
    except requests.exceptions.ConnectionError as err:
        error_msg = _create_connection_error(str(err))
        return RoxResponse(False, error_msg)

    if r.status_code != 200:
        error_msg = _create_http_status_error(r.status_code, r.text)
        return RoxResponse(False, error_msg)
    else:
        return RoxResponse(True, r.text)


def start_service(service_json: dict) -> RoxResponse:
    """
    Start service defined by given JSON dictionary.
    :param service_json: JSON dictionary defining service.
    :return: Result dictionary documenting if service could be started.
    """
    if not service_json:
        # JSON data is empty and therefore invalid.
        return RoxResponse(False, MSG_MISSING_SERVICES_ERROR)

    url = "http://{}/start_service".format(rox_connector_url)

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
    :return: Result dictionary documenting which services could not be started.
    """
    not_started_json_list = []
    if len(service_json_list) < 1:
        # Service list is empty and therefore invalid.
        res = RoxResponse(False, MSG_MISSING_SERVICES_ERROR)
        res.data = not_started_json_list
        return res

    all_services_started = True
    for service_json in service_json_list:
        res = start_service(service_json)
        if not res.success:
            not_started_json_list.append(service_json["params"]["name"])
            all_services_started = False

    res = RoxResponse(all_services_started, "")
    res.data = not_started_json_list

    return res


def shutdown_service(service_name: dict) -> RoxResponse:
    """
    Stop service defined by given name.
    :param service_name: Service name.
    :return: Result dictionary documenting if service could be stopped.
    """
    if not service_name:
        # Service name is empty and therefore invalid.
        return RoxResponse(False, MSG_MISSING_SERVICES_ERROR)

    content = {'name': service_name}
    url = "http://{}/shutdown_service".format(rox_connector_url)

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
    :return: Result dictionary documenting which services could not be stopped.
    """
    not_stopped_name_list = []
    if len(service_name_list) < 1:
        # Service list is empty and therefore invalid.
        res = RoxResponse(False, MSG_MISSING_SERVICES_ERROR)
        res.data= not_stopped_name_list
        return res

    all_services_stopped = True
    for service_name in service_name_list:
        res = shutdown_service(service_name)
        if not res.success:
            not_stopped_name_list.append(service_name)
            all_services_stopped = False
    res = RoxResponse(all_services_stopped, "")
    res.data = not_stopped_name_list
    return res


def get_running_services() -> list:
    """
    get a list of all registered services (as strings)
    :returns: list of running services
    """

    url = "http://{}/services".format(rox_connector_url)

    try:
        r = requests.get(url)
    except requests.exceptions.ConnectionError as e:
        logging.error("ERROR: no connection to server - {}".format(e))
        return []
    except Exception as e:
        logging.error("ERROR: {}".format(e))

    if r.status_code == 200:
        services = list(r.json().keys())
        logging.info('currently running services: ' + str(services))
        return services
    else:
        logging.error('ERROR: {} - {}'.format(r.status_code, r.text))
        return []


def set_pipeline(pipeline_name: str, service_names: list) -> bool:
    """
    Create new pipeline with specified services in exactly the given order.
    :param pipeline_name: Name of pipeline.
    :param service_names: A list of service names. The services
    are applied in the same order as they appear in this list.
    :returns: True if pipeline could be created an False otherwise.
    """

    url = "http://{}/set_pipeline".format(rox_connector_url)
    content = {'name': pipeline_name, 'services': service_names}
    logging.error("Halllo" + str(service_names))

    try:
        r = requests.post(url, data=json.dumps(content), headers=JSON_HEADER)
    except requests.exceptions.ConnectionError as err:
        logger.error("{}\n{}".format(MSG_CONNECTION_ERROR, err))
        return False

    if r.status_code != 200:
        logger.error("Pipeline could not be created. Error code {}.\n{}".format(r.status_code, r.text))
        return False
    else:
        return True


def remove_pipeline():  # TODO
    pass


def get_pipelines() -> dict:
    """
    Get metadata of each available pipeline, i.e. pipeline name, involved services and current status.
    :returns: Pipeline metadata as JSON dictionary. May be empty in case of an error.
    """

    url = "http://{}/pipelines".format(rox_connector_url)

    try:
        r = requests.get(url)
    except requests.exceptions.ConnectionError as err:
        logging.error("{}\n{}".format(MSG_CONNECTION_ERROR, err))
        return {}

    if r.status_code != 200:
        logging.error("Pipelines could not be received. Error code {}.\n{}".format(r.status_code, r.text))
        return {}
    else:
        return r.json()


def dump_everything(file_name):
    """Save current session to specified file"""
    file_name = os.path.join(rox_composer_dir, file_name)
    f = None
    try:
        f = open(file_name, 'w')
    except Exception as e:
        err = 'ERROR unable to open file {} - {}'.format(file_name, e)
        logging.error(err)
        return RoxResponse(False, err)

    try:
        r = requests.get('http://{}/dump_services_and_pipelines'.format(rox_connector_url))
    except requests.exceptions.ConnectionError as e:
        err = "{}\n{}".format(MSG_CONNECTION_ERROR, e)
        logging.error(err)
        return RoxResponse(False, err)

    if r.status_code == 200:
        o = r.json()
        try:
            json.dump(o, f)
        except Exception as e:
            err = 'ERROR: unable to write dump to file {} - {}'.format(file_name, e)
            logging.error(err)
            return RoxResponse(False, err)
        finally:
            f.close()

        return RoxResponse(True, "dump written to file {}\n{}".format(file_name, r.text))
    else:
        f.close()
        err = 'ERROR: {} - {}'.format(r.status_code, r.text)
        logging.error(err)
        return RoxResponse(False, err)


def restore_session(file_name):
    """ restore a saved session """
    session_file = os.path.join(rox_composer_dir, file_name)
    if os.path.isfile(session_file):
        f = open(session_file, "r")
        restore_json = json.loads(f.read())
        f.close()

    else:
        err = 'file {} not found'.format(file_name)
        logging.error(err)
        return RoxResponse(False, err)

    r = requests.post('http://{}/load_services_and_pipelines'.format(rox_connector_url), data=json.dumps(restore_json),
                      headers=JSON_HEADER)
    if r.status_code == 200:
        return RoxResponse(True, r.text)
    else:
        err = 'ERROR: {} - {}'.format(r.status_code, r.text)
        logging.error(err)
        return RoxResponse(False, err)


def watch_services(service_names, session = None, timeout = SESSION_TIMEOUT):
    """

    :param service_names: List of Names of the services to watch
    :param session: A dictionary with an id, a timeout and a set of services that are being watched.
    :return: Tuple (bool, str, dict): True if watch service worked, String is message from server and dict the session
    """

    #if there is no session yet start new session
    if session is None:
        session = dict()
        session['services'] = set()
        session['timeout'] = timeout

        services = ", ".join(service_names)
        data = {'lines': 100, 'timeout': timeout, 'services': services}
        try:
            r = requests.put('http://{}/log_observer'.format(rox_connector_url), headers=JSON_HEADER, json=data)
        except requests.exceptions.ConnectionError as e:
            err = "ERROR: no connection to server - {}".format(e)
            logging.error(err)
            return RoxResponse(False, err)

        if r.status_code != 200:
            err = 'ERROR: {}'.format(r.text)
            logging.error(err)
            return RoxResponse(False, err)

        session['id'] = r.json()['sessionid']

        for s in services:
            session['services'].add(s)

        res = RoxResponse(True, r.text)
        res.data = session
        return res

    else:
        unwatched_services = list(session['services'] - set(service_names))

        if unwatched_services:
            #services = ", ".join(unwatched_services)
            data = {'sessionid': session['id'], 'services': unwatched_services}
            try:
                r = requests.post('http://{}/log_observer'.format(rox_connector_url), headers=JSON_HEADER, json=data)
            except requests.exceptions.ConnectionError as e:
                err = "ERROR: no connection to server - {}".format(e)
                logging.error(err)
                res = RoxResponse(False, err)
                res.data=session
                return res

            if r.status_code != 200:
                err = 'ERROR: {}'.format(r.text)
                logging.error(err)
                res = RoxResponse(False, err)
                res.data = session
                return res

            response = r.json()
            for s in response['ok']:
                session['services'].add(s)

            res = RoxResponse(True, r.text)
            res.data = session
            return res


def get_service_logs():
    pass


def unwatch_services():  # TODO
    pass


def watch_pipelines():  # TODO
    pass


def unwatch_pipelines():  # TODO
    pass


def watch_all():  # TODO
    pass


def reset_watchers():  # TODO
    pass


def get_service_logs(session):
    """

    :return:
    """
    if session is None:
        raise RuntimeError('no services are currently under observation')

    data = {'sessionid': session['id']}
    try:
        r = requests.get('http://{}/log_observer'.format(rox_connector_url), headers=JSON_HEADER, json=data)
    except requests.exceptions.ConnectionError as e:
        return "ERROR: no connection to server - {}".format(e)

    if r.status_code != 200:
        raise RuntimeError(r.text)

    return "\n".join(r.json()['loglines'])


def save_pipeline(file_name):  # TODO
    pass


def load_and_start_pipeline(pipe_path):  # TODO
    d = {'pipe_path': pipe_path}
    r = requests.post('http://{}/load_and_start_pipeline'.format(rox_connector_url), data=json.dumps(d),
                      headers=JSON_HEADER)
    if r.status_code == 200:
        msg = r.text
        logging.info(msg)
        return RoxResponse(True, msg)
    else:
        err = 'ERROR: {} - {}'.format(r.status_code, r.text)
        return RoxResponse(False, err)
