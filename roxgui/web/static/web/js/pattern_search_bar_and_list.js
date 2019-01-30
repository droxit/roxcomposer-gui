/* encoding: utf-8
#
# Define the patterns of a search bar with a searchable list.
#
# devs@droxit.de
#
# Copyright (c) 2019 droxIT GmbH
#
*/

function get_option_text_pattern() {
	return 'option_';
}

function get_info_text_pattern() {
	return 'info_';
}

function create_option_id(data_name) {
	var option_text_pattern = get_option_text_pattern();
	return option_text_pattern + data_name;
}

function create_info_id(data_name) {
	var info_text_pattern = get_info_text_pattern();
	return info_text_pattern + data_name;
}

function extract_name_from_info_id(info_id) {
	return info_id.replace(get_info_text_pattern(), '');
}

function add_data_entry(search_field, func, data_name, data_info, info_container) {
	// Append entry to data name list.
	var option = document.createElement('option');
	option.setAttribute('id', create_option_id(data_name));
	option.setAttribute('data-info', data_info)
	option.appendChild(document.createTextNode(data_name));
	search_field.list.appendChild(option);

	// Append entry to data info list.
	if(info_container != null){
	    var li = document.createElement('li');
        li.setAttribute("id", create_info_id(data_name));
        li.setAttribute("class", "list-group-item");
        li.setAttribute("title", data_info);
        li.setAttribute("data-title", data_info);
        li.setAttribute("data-name", data_name);
        li.setAttribute("onclick", func); //go_to_detail_view(this)
        li.appendChild(document.createTextNode(data_name));
        info_container.appendChild(li);
	}

}

function add_data_entries(search_field, func, name_info_list, info_container) {
    if(info_container != null){
        info_container.innerHTML = "";
    }
	for (var i = 0; i < name_info_list.length; i++) {
		var name = name_info_list[i][0];
		var info = name_info_list[i][1];
		add_data_entry(search_field, func, name, info, info_container);
	}
}


function add_data_entries_from_remote(search_field, func, info_container, relative_url) {
    var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
	$.post(relative_url, {
	    csrfmiddlewaretoken: CSRFtoken,
	}).done(function(data) {
	    // Create list to store converted data.
	    name_info_list = [];
	    // Convert JSON data to string.
	    for (var i in data) {
	        var name = i;
	        var json = convert_to_json_string(data[i]);
	        name_info_list.push([name, json]);
	    }
	    // Add service data to list.
	    add_data_entries(search_field, func, name_info_list, info_container);
	});
}

function remove_data_entry(data_name) {
	// Remove entry from data name list.
	document.getElementById(create_option_id(data_name)).remove();
	// Remove entry from data info list.
	document.getElementById(create_info_id(data_name)).remove();
}

function remove_all_data_entries() {
	// Remove all entries from data name list.
	var name_list = document.getElementById('data_name_list');
	while (name_list.firstChild) {
		name_list.removeChild(name_list.firstChild);
	}
	// Remove all entries from data info list.
	var info_list = document.getElementById('data_info_list');
	while (info_list.firstChild) {
		info_list.removeChild(info_list.firstChild);
	}
}

function set_hidden_status(elem, hidden_status) {
	if (elem != null && (typeof hidden_status == 'boolean')) {
		if (hidden_status) {
			elem.style.display = 'none';
		} else {
			elem.style.display = 'block';
		}
	}
}

function set_single_hidden_status(data_name, hidden_status) {
	if (data_name != null && data_name != "" && (typeof hidden_status == 'boolean')) {
		var elem = document.getElementById(create_info_id(data_name));
		set_hidden_status(elem, hidden_status);
	}
}

function set_all_hidden_status(elem_list, hidden_status) {
	if (elem_list != null && (typeof hidden_status == 'boolean')) {
		elem_list.childNodes.forEach(function(elem) {
		    set_hidden_status(elem, hidden_status);
		});
	}
}

function search_data_list() {
	// Get current entry in search bar.
	var keyword = document.getElementById('search_field').value;
	// Get current data info list.
	var name_list = document.getElementById('data_info_list');

	// Handle empty keywords.
	if (keyword == null || keyword == "") {
		// Keyword is empty, so restore list.
		set_all_hidden_status(name_list, false);
		return;
	}

	// Extract data name and corresponding info for
	// each entry and store them in separate list.
	var data_list = [];
	var child_list = Array.from(name_list.childNodes);
	child_list.forEach(function(item) {
		var name = extract_name_from_info_id(item.id);
		var info = item.title;
		data_list.push([name, info]);
	});

	// Define search function for current data structure.
	function search_name_and_info(elem, pattern) {
		var name = elem[0];
		var info = elem[1];
		return (name.includes(pattern) || info.includes(pattern));
	}

	// Process searching and store results.
	tuple_list = custom_keyword_search(data_list, keyword, search_name_and_info);

	// Update list correspondingly.
	set_all_hidden_status(name_list, true);
	tuple_list.forEach(function(tuple) {
	    var name = tuple[0];
		set_single_hidden_status(name, false);
	});
}
