# encoding: utf-8
#
# Class encapsulating ROXconnector response.
#
# |------------------- OPEN SOURCE LICENSE DISCLAIMER -------------------|
# |                                                                      |
# | Copyright (C) 2019  droxIT GmbH - devs@droxit.de                     |
# |                                                                      |
# | This file is part of ROXcomposer GUI.                                |
# |                                                                      |
# | ROXcomposer GUI is free software:                                    |
# | you can redistribute it and/or modify                                |
# | it under the terms of the GNU General Public License as published by |
# | the Free Software Foundation, either version 3 of the License, or    |
# | (at your option) any later version.                                  |
# |                                                                      |
# | This program is distributed in the hope that it will be useful,      |
# | but WITHOUT ANY WARRANTY; without even the implied warranty of       |
# | MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the         |
# | GNU General Public License for more details.                         |
# |                                                                      |
# | You have received a copy of the GNU General Public License           |
# | along with this program. See also <http://www.gnu.org/licenses/>.    |
# |                                                                      |
# |----------------------------------------------------------------------|
#


class RoxResponse:
    """
    Class encapsulating a ROXconnector response.
    Each response contains a flag to indicate whether
    or not the requested operation has been successful
    and a string with corresponding response message.
    Optional attributes are data in case information
    has been requested from the server and error data
    that might be provided to mark erroneous data.
    """

    def __init__(self, success: bool, message: str = ""):
        self.success = success
        self.message = message
        # (Optional) data concerning successful request.
        self._data = []
        # (Optional) data concerning failing request.
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
