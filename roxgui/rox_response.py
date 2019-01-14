# encoding: utf-8
#
# Class encapsulating ROXconnector response.
#
# devs@droxit.de
#
# Copyright (c) 2019 droxIT GmbH
#


class RoxResponse:
    """
    Class encapsulating ROXconnector response.
    Each response has to have a status indicating whether the communication and
    requested operation has been successful and a message that is sent by the ROXconnector.
    Optional parameters are data in case information has been requested from the server
    and error data that can be provided if an error has occured.
    """

    def __init__(self, success: bool, message: str = ""):
        self.success = success
        self.message = message
        # (Optional) data concerning successful request.
        self._data = []
        # (Optional) data concerning failed request.
        self._error_data = []

    # Getter and setter.
    # ==================

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, new_data):
        self._data = new_data

    @property
    def error_data(self):
        return self._error_data

    @error_data.setter
    def error_data(self, new_data):
        self._error_data = new_data

    def __str__(self):
        return "RoxResponse status: {}, Msg: {}, Data: {} ".format(self.success, self.message, self.data)

    def convert_to_json(self) -> dict:
        """
        Convert current instance to JSON dictionary.
        :return: Current instance as JSON dictionary.
        """
        json_dict = {
            "success": self.success,
            "message": self.message,
            "data": self.data,
            "error_data": self.error_data
        }
        return json_dict
