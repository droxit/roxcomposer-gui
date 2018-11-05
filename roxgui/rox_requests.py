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


def post_to_pipeline(pipeline, message):
    """
    Post a message to the pipeline
    :param pipeline: the pipeline name that the message is to be sent to
    :param message: a string
    :return: True if message was sent
    """
    d = {'name': pipeline, 'data': message}
    try:
        r = requests.post('http://{}/post_to_pipeline'.format(rox_connector_url), data=json.dumps(d),
                          headers=JSON_HEADER)
    except requests.exceptions.ConnectionError as err:
        logging.error("{}\n{}".format(MSG_CONNECTION_ERROR, err))
        return False, "{}\n{}".format(MSG_CONNECTION_ERROR, err)

    if r.status_code == 200:
        logging.info("Posted message: {}".format(message))
        msg_id = r.json()['message_id']
        msg = "Message posted - ID: {} ".format(msg_id)
        return True, msg
    else:
        msg = 'ERROR: {} - {}'.format(r.status_code, r.text)
        logging.error(msg)
        return False, msg


def get_msg_history(msg_id):
    d = {'message_id': msg_id}

    try:
        r = requests.post('http://{}/get_msg_history'.format(rox_connector_url), data=json.dumps(d), headers=JSON_HEADER)
    except requests.exceptions.ConnectionError as e:
        err = "ERROR: no connection to server - {}".format(e)
        logging.error(err)
        return False, err
    if r.status_code == 200:
        logging.info(r.text)
        return True, r.text
    else:
        err = 'ERROR: {} - {}'.format(r.status_code, r.text)
        logging.error(err)
        return False, err


def start_service(service_json: dict) -> bool:
    """
    Start service defined by given JSON dictionary.
    :param service_json: JSON dictionary defining service.
    :return: True if service could be started and False otherwise.
    """
    if not service_json:
        # JSON data is empty and therefore invalid.
        return False

    url = "http://{}/start_service".format(rox_connector_url)

    try:
        r = requests.post(url, json=service_json, headers=JSON_HEADER)
    except requests.exceptions.ConnectionError as err:
        logging.error("{}\n{}".format(MSG_CONNECTION_ERROR, err))
        return False, "{}\n{}".format(MSG_CONNECTION_ERROR, err)
    if r.status_code != 200:
        logging.error("Service could not be started. Error code {}.\n{}".format(r.status_code, r.text))
        return False, "Service could not be started. Error code {}.\n{}".format(r.status_code, r.text)
    else:
        return True, ""


def start_services(service_json_list: list) -> list:
    """
    Start all services defined by given list of JSON dictionaries.
    :param service_json_list: List of JSON dictionaries defining multiple services.
    :return: List of JSON dictionaries representing all services which could not be started.
    """
    error_json_list = []
    delivered = True
    if len(service_json_list) < 1:
        # Service list is empty and therefore invalid.
        return False, ["Please select a service to start."]

    for service_json in service_json_list:
        delivered, result = start_service(service_json)
        if not delivered:
            error_json_list.append("Service could not be started: {} \n Error: {}".format(service_json, result))
            delivered = False

    return delivered, error_json_list


def shutdown_service(service_name: dict) -> bool:
    """
    Stop service defined by given name.
    :param service_name: Service name.
    :return: True if service could be stopped and False otherwise.
    """
    if not service_name:
        # Service name is empty and therefore invalid.
        return False

    url = "http://{}/shutdown_service".format(rox_connector_url)
    data = {'name': service_name}

    try:
        r = requests.post(url, json=data, headers=JSON_HEADER)
    except requests.exceptions.ConnectionError as err:
        logger.error("{}\n{}".format(MSG_CONNECTION_ERROR, err))
        return False
    if r.status_code != 200:
        logging.error("Service could not be stopped. Error code {}.\n{}".format(r.status_code, r.text))
        return False
    else:
        return True


def shutdown_services(service_name_list: list) -> list:
    """
    Stop all services defined by given list of service names.
    :param service_name_list: List of service names.
    :return: List of service names which could not be stopped.
    """
    error_name_list = []
    if len(service_name_list) < 1:
        # Service list is empty and therefore invalid.
        return error_name_list

    for service_name in service_name_list:
        result = shutdown_service(service_name)
        if not result:
            error_name_list.append(service_name)
    return error_name_list


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


def set_pipeline(pipename: str, services: list) -> bool:
    """
    create a new pipeline with the specified services, where the order is important
    :param pipename: Name of the Pipeline
    :param services: a list of service names (string) that should be added to the pipeline
    :returns: True if pipeline was sent
    """

    d = {'name': pipename, 'services': services}
    headers = {'Content-Type': 'application/json'}
    try:
        r = requests.post('http://{}/set_pipeline'.format(rox_connector_url), data=json.dumps(d), headers=headers)
    except requests.exceptions.ConnectionError as e:
        logging.error("ERROR: no connection to server - {}".format(e))
        return False

    if r.status_code == 200:
        logging.info("Pipeline sent, Response: " + r.text)
        return True
    else:
        logging.error('ERROR: {} - {}'.format(r.status_code, r.text))
        return False


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
        return False, err

    try:
        r = requests.get('http://{}/dump_services_and_pipelines'.format(rox_connector_url))
    except requests.exceptions.ConnectionError as e:
        err = "{}\n{}".format(MSG_CONNECTION_ERROR, e)
        logging.error(err)
        return False, err

    if r.status_code == 200:
        o = r.json()
        try:
            json.dump(o, f)
        except Exception as e:
            err = 'ERROR: unable to write dump to file {} - {}'.format(file_name, e)
            logging.error(err)
            return False, err
        finally:
            f.close()

        return True, "dump written to file {}\n{}".format(file_name, r.text)
    else:
        f.close()
        err = 'ERROR: {} - {}'.format(r.status_code, r.text)
        logging.error(err)
        return False, err


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
        return False, err

    r = requests.post('http://{}/load_services_and_pipelines'.format(rox_connector_url), data=json.dumps(restore_json),
                      headers=JSON_HEADER)
    if r.status_code == 200:
        return True, r.text
    else:
        err = 'ERROR: {} - {}'.format(r.status_code, r.text)
        logging.error(err)
        return False, err

def watch_services():  # TODO
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


def get_service_logs():  # TODO
    pass

def save_pipeline(file_name): #TODO
    pass

def load_and_start_pipeline(pipe_path):  # TODO
    d = {'pipe_path': pipe_path}
    r = requests.post('http://{}/load_and_start_pipeline'.format(rox_connector_url), data=json.dumps(d), headers=JSON_HEADER)
    if r.status_code == 200:
        msg = r.text
        logging.info(msg)
        return True, msg
    else:
        err = 'ERROR: {} - {}'.format(r.status_code, r.text)
        return False, err