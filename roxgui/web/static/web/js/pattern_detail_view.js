/*
#
# Define the pattern for a detail view that is similar for services and pipelines.
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

/* Creates the headline of the detail view (which is set to 'select a service/pipe' if nothing is selected) */
function create_headline(name) {
	var detail_info = $("#detail_info")[0];
	detail_info.dataset.name = name;

	var headline = document.createElement("div");
	headline.setAttribute("id", "headline_detail");
	headline.setAttribute("onclick", "edit_detail_headline()");
	headline.setAttribute("data-name", name);

	var header = document.createElement("h4");
	header.appendChild(document.createTextNode(name));
	headline.appendChild(header);
	return headline;
}

/* Setter for the headline of the detail view. */
function set_detail_headline(val) {
	var headline = $("#headline_detail");
	var new_headline = create_headline(val);
	headline.replaceWith(new_headline);

	var detail_info = $("#detail_info")[0];
	detail_info.dataset.name = val;
}


/* When the headline is clicked an input field is created.
    After entering the new string it will be saved as the new headline. */
function edit_detail_headline(btn) {
	var headline = $("#headline_detail")[0];
	var detail_info = $("#detail_info")[0];

	var current_name = detail_info.dataset.name;
	create_input_field(headline, current_name, create_headline); //in pattern_input_field

}

/* When an editable parameter field is clicked this function is called. Creates a text area (for long texts). */
function edit_param_textarea(param_div, param) {

	create_textarea(param_div, param, create_param_textarea);
}

/* When an editable parameter field is clicked this function is called. */
function edit_param_field(param_div, param) {

	create_input_field(param_div, param, create_param_field);
}

/* When an editable parameter field is clicked this function is called. */
function edit_param_field_headline(param_div, param) {

	create_input_field(param_div, param, create_param_field_headline);
}

/* A new editable parameter field is created. */
function create_param_textarea(val) {
	return create_param_general('edit_param_textarea', set_param_field, val);
}

/* A new editable parameter field is created. */
function create_param_field(val) {
	return create_param_general('edit_param_field', set_param_field, val);
}

/* Save the new content of the editable parameter field. */
function set_param_field(param_val) {
	var new_text_field = document.createTextNode(param_val);
	return new_text_field;

}

/* A new editable parameter field is created. */
function create_param_field_headline(val) {
	return create_param_general('edit_param_field_headline', set_param_field_headline, val);
}

/* Save the new content of the editable parameter field as a headline. */
function set_param_field_headline(param_val) {
	var new_text_field = document.createElement("h4");
	new_text_field.appendChild(document.createTextNode(param_val));
	return new_text_field;

}

function create_param_general(func_string, func, val) {
	var param_div = document.createElement("div");
	param_div.setAttribute("onclick", func_string + "(this, '" + val + "')");

	var param_content = func(val);
	param_div.appendChild(param_content);
	return param_div
}


/* Called when an element from the list is selected to show the detail
    view containing information on the selected element. */
function go_to_detail_view(elem) {
	set_detail_headline(elem.dataset.name);
	enable_detail_elements();

	var detail_view = create_detail_view(elem.dataset.name);
	add_detail_view(detail_view);

	var detail_info = $("#detail_info")[0];
	set_buttons(detail_info);
}

/* Called when a new pipe/service is to be created, a new empty detail view is opened
    And the buttons and input elements are set from disabled to enabled. */
function go_to_new_detail_view(new_name) {
	set_detail_headline(new_name);
	enable_detail_elements();

	var detail_view = create_detail_view(new_name);
	add_detail_view(detail_view);

	var detail_info = $("#detail_info")[0];
	set_buttons(detail_info);

}

/* Add the new detail view to the container. */
function add_detail_view(elem) {
	var detail_view = $("#data_detail_list");
	detail_view.html("");
	detail_view[0].appendChild(elem);
}

/* Pattern to toggle a button. Func_enable is called if the buttons status is set to 0, func_disable else.
    info contains information such as 'name' e.g. when a service is started. */
function toggle_services(info, btn, func_enable, func_disable) {
	if (!check_disabled(btn)) {
		if (btn.dataset.status == "0") {
			func_enable(info);
		} else if (btn.dataset.status == "1") {
			func_disable(info);
		}
	}
}

/* Pattern to toggle the run button. */
function toggle_run_button(btn, btn_status, tooltip_off, tooltip_on) {
	toggle_button(btn, btn_status, "fa-play", "fa-stop", tooltip_off, tooltip_on);
}

/* Pattern to toggle the watch button. */
function toggle_watch_button(btn, btn_status, tooltip_off, tooltip_on) {
	toggle_button(btn, btn_status, "fa-eye", "fa-eye-slash", tooltip_off, tooltip_on);
}
