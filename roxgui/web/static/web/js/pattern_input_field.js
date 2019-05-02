/*
#
# Define the the pattern of an editable input field (editable when clicked).
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
*/

/* Create an editable input field. */
function create_input_field(text_node, placeholder, change_text_node) {

	var input_field = document.createElement("input");
	create_editable_element(input_field, text_node, placeholder, change_text_node);
}

/* Create an editable text field. */
function create_textarea(text_node, placeholder, change_text_node) {

	var input_field = document.createElement("textarea");
	create_editable_element(input_field, text_node, placeholder, change_text_node);

}


/*  Create a new editable input field from an existing text node
    text_node is the place where the input field should reside (the text that gets replaced)
    placeholder is the text that was in the textnode first
    new_info_container is an html element with the correct format for the new output */
function create_editable_element(input_field, text_node, placeholder, change_text_node) {
	input_field.setAttribute("type", "text");
	input_field.setAttribute("placeholder", placeholder);
	input_field.setAttribute("class", "form-control");
	input_field.setAttribute("id", text_node.id);
	input_field.value = placeholder;
	var old_name = ""

    if(text_node.dataset.old_name){
        old_name = text_node.dataset.old_name;
        input_field.dataset.old_name = old_name
    }


	input_field.addEventListener("keyup", function(e) {
		e.preventDefault();
		if (e.keyCode == 13) {
			input_save(input_field, placeholder, change_text_node);
		}
	});

	input_field.addEventListener("focusout", function(e) {
		e.preventDefault();
		if (input_field) {
			input_save(input_field, placeholder, change_text_node);
		}
	});

	text_node.replaceWith(input_field);
	input_field.focus();
}

/* Save the new content of the input field (input field vanishes and is replaced with a text node again) */
function input_save(input_field, placeholder, change_text_node) {
	var new_info = input_field.value;
	if (!new_info) {
		new_info = placeholder;
	}
	var new_text_node = change_text_node(new_info);
	if(input_field.dataset.old_name)
	    new_text_node.dataset.old_name = input_field.dataset.old_name
	input_field.replaceWith(new_text_node);
}
