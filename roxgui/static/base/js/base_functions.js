/*
# JavaScript functions that are needed throughout the whole site.
#
# |------------------- OPEN SOURCE LICENSE DISCLAIMER -------------------|
# |                                                                      |
# | Copyright (C) 2019  droxIT GmbH - devs@droxit.de                     |
# |                                                                      |
# | This file is part of ROXcomposer.                                    |
# |                                                                      |
# | ROXcomposer is free software: you can redistribute it and/or modify  |
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
*/

/* Search for keywords in list of strings. */
function keyword_search(search_list, item) {
	if (search_list != null && item != null && item != "") {
		return search_list.filter(function(list_item) {
			return list_item.includes(item);
		});
	} else {
		return [];
	}
}

/* Search for keywords in custom data structure. */
function custom_keyword_search(search_list, item, condition) {
	if (search_list != null && item != null && item != "" && condition != null) {
		result_list = [];
		search_list.forEach(function(container) {
			if (condition(container, item)) {
				result_list.push(container);
			}
		})
		return result_list;
	} else {
		return [];
	}
}

/* Sort given list of numbers or strings in alphabetical order. */
function alphabetical_sort(sort_list) {
	if (sort_list != null) {
		return sort_list.sort(function(a, b) {
			if (a < b) {
				return -1;
			}
			if (a > b) {
				return 1;
			}
			return 0;
		});
	} else {
		return [];
	}
}

/* Convert JSON instance to properly formatted string. */
function convert_to_json_string(json_instance) {
	json_string = JSON.stringify(json_instance, null, '\t');
	return json_string;
}

function escapeHtml(unsafe) {
	unsafe = unsafe.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/'"'/g, "&quot;").replace(/"'"/g, "&#039;");
	unsafe = unsafe.replace(/\\n/g, "\\n")
		.replace(/\\'/g, "\\'")
		.replace(/\\"/g, '\\"')
		.replace(/\\&/g, "\\&")
		.replace(/\\r/g, "\\r")
		.replace(/\\t/g, "\\t")
		.replace(/\\b/g, "\\b")
		.replace(/\\f/g, "\\f");
	unsafe = unsafe.replace(/[\u0000-\u0019]+/g, "");
	return unsafe
}

function set_tooltip(elem, tooltip) {
	elem.toggle = "tooltip";
	elem.placement = "bottom";
	elem.title = tooltip;
}

/* Convert JSON to a string without slashes or ticks */
function stringify(obj_from_json) {
	if (typeof obj_from_json !== "object" || Array.isArray(obj_from_json)) {
		// not an object, stringify using native function
		return JSON.stringify(obj_from_json);
	}
	// Implements recursive object serialization according to JSON spec
	// but without quotes around the keys.
	let props = Object
		.keys(obj_from_json)
		.map(key => `${key}:${stringify(obj_from_json[key])}`)
		.join(",");
	return `{${props}}`;
}
