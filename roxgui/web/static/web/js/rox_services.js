/* encoding: utf-8
#
# Define the services functionality of the services page.
#
# devs@droxit.de
#
# Copyright (c) 2019 droxIT GmbH
#
*/


/* This function is called when the service view is first opened and no service is selected
    It shows an empty detail view with disabled buttons */
function show_empty_detail_view() {
	$("#data_detail_list").html("");
	var detail_headline = $("#headline_detail");
	detail_headline[0].setAttribute("onclick", "");

	detail_headline.html("<h4>Select a service.</h4>");
}

/* Set the tooltips for all buttons on the services page. */
function set_service_tooltips() {
	set_service_tooltip($("#btn-watch")[0].dataset, "watch service");
	set_service_tooltip($("#btn-edit")[0].dataset, "edit name");
	set_service_tooltip($("#btn-run")[0].dataset, "start service");
	set_service_tooltip($("#btn-delete")[0].dataset, "delete service");
	set_service_tooltip($("#btn-save")[0].dataset, "save changes");
	set_service_tooltip($("#btn-add")[0].dataset, "add new service");
}

/* Set the tooltip for a single button.
    Also, the status is initialized to 0 as this function is only called when opening the service page anew */
function set_service_tooltip(btn, tooltip) {
	btn.status = "0";
	set_tooltip(btn, tooltip);
}

/* Enable certain buttons that already have functionality. */
function enable_detail_elements() {
	//"btn-watch" ,"btn-delete", "btn-save"
	["btn-edit", "btn-run", "btn-watch"].forEach(function(btn) {
		btn_remove_disabled(btn);
	});
}

/* Removes the disabled status on an element*/
function btn_remove_disabled(btn) {
	var btnedit = $("#" + btn + "")[0];
	btnedit.classList.remove("disabled");
}

/* Retrieves the hidden info dataset*/
function get_dataset() {
	return $("#detail_info")[0].dataset;
}

/* Sets the hidden dataset information */
function set_service_info(elem) {
	var dataset = get_dataset();
	var service = elem.dataset.name;
	dataset.name = service;
	dataset.services = [elem.dataset.name];
	dataset.title = elem.dataset.title;
}

/* When a service has been selected this function is called to create the detail view of this service. */
function create_detail_view(service) {
	var detail_container = document.createElement("div");
	detail_container.setAttribute("class", "container");
	detail_container.setAttribute("id", "detail-container")

	var empty_row = document.createElement("div");
	empty_row.setAttribute("class", "row");
	var empty_col = document.createElement("div");
	empty_col.setAttribute("class", "col-md-12");
	empty_col.appendChild(document.createElement("p"));
	empty_row.appendChild(empty_col);
	detail_container.appendChild(empty_row);

	if (service === "") {
		// Service name is not given, so create empty detail view.
		get_empty_params(detail_container);
		var plus_btn = document.createElement("button");
		plus_btn.setAttribute("class", "btn btn-primary");
		plus_btn.onclick = () => append_param(detail_container, "key", "value");
		var plus_span = document.createElement("span");
		plus_span.setAttribute("class", "fas fa-plus")
		plus_btn.appendChild(plus_span);
		detail_container.appendChild(plus_btn);
		var minus_btn = document.createElement("button");
		minus_btn.setAttribute("class", "btn btn-primary");
		minus_btn.onclick = () => delete_last_param(detail_container);
		var minus_span = document.createElement("span");
		minus_span.setAttribute("class", "fas fa-minus")
		minus_btn.appendChild(minus_span);
		detail_container.appendChild(minus_btn);
	} else {
		// Service name is given, so add corresponding parameters in detail view.
		get_params(detail_container, service);
	}

	return detail_container;

}

/* append an editable key value pair to the container */
function append_param(container, key, val) {
	var row = document.createElement("div");
	row.setAttribute("class", "row");
	container.appendChild(row);

	var col1 = document.createElement("div");
	col1.setAttribute("class", "col-md-5");
	col1.setAttribute("align", "center");

	var col2 = document.createElement("div");
	col2.setAttribute("class", "col-md-1");
	col2.setAttribute("align", "center");

	var col3 = document.createElement("div");
	col3.setAttribute("class", "col-md-5");
	col3.setAttribute("align", "center");

	row.appendChild(col1);
	row.appendChild(col2);
	row.appendChild(col3);

	var param_field_key = create_param_field(key);
	var param_field_value = create_param_field(val);
	col1.appendChild(param_field_key);
	col2.appendChild(document.createTextNode(" : "));
	col3.appendChild(param_field_value);
}

function delete_last_param(container) {
	var detail_container = document.querySelector("#detail-container");
	var last_child = detail_container.lastChild;
	var cols = last_child.querySelectorAll(".col-md-5 h4");
	if (cols.length == 2) {
		detail_container.removeChild(last_child);
	}
}

/* Retrieve the parameter key-value pairs of a service from the hidden dataset */
function get_params(container, service) {
	var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
	$.post("get_service_info", {
		services: [service],
		csrfmiddlewaretoken: CSRFtoken
	}).done(function(data) {

		var json_params = data[service];

		if (json_params.classpath) {
			var key = "classpath";
			var val = json_params.classpath;
			append_param(container, key, val);
		}
		if (json_params.ip) {
			var key = "ip";
			var val = json_params.ip;
			append_param(container, key, val);
		}
		if (json_params.port) {
			var key = "port";
			var val = JSON.stringify(json_params.port);
			append_param(container, key, val);
		}
		if (json_params.name) {
			var key = "name";
			var val = json_params.name;
			append_param(container, key, val);
		}

		jQuery.each(json_params.params, function(i, val) {
			if (typeof val === 'string' || val instanceof String) {
				value = val;
			} else {
				value = escapeHtml(convert_to_json_string(val));
			}
			append_param(container, i, val);
		});
	});
}

function get_empty_params(container) {
	append_param(container, "classpath", "new classpath");
	append_param(container, "ip", "new ip");
	append_param(container, "port", "new port");
	append_param(container, "name", "new name");
}

function save_detail() {
	// Get detail container.
	var detail_container = document.querySelector("#detail-container");
	// Iterate through its child nodes, each
	// containing a single key value pair.
	classpath_value = null;
	ip_value = null;
	port_value = null;
	name_value = null;
	key_array = []
	value_array = []
	for (var i = 0; i < detail_container.childNodes.length; i++) {
		var child = detail_container.childNodes[i];
		var cols = child.querySelectorAll(".col-md-5 h4");
		if (cols.length == 2) {
			key = cols[0].innerText;
			value = cols[1].innerText;
			if (key == "classpath") {
				classpath_value = value;
			} else if (key == "port") {
				port_value = value;
			} else if (key == "ip") {
				ip_value = value;
			} else if (key == "name") {
				name_value = value;
			} else {
				key_array.push(key);
				value_array.push(value);
			}
		}
	}

	// Send parameters to backend in order to create specified service.
	var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
	$.post("create_service", {
		"classpath": classpath_value,
		"ip": ip_value,
		"port": port_value,
		"name": name_value,
		"optional_param_keys": key_array,
		"optional_param_values": value_array,
		"csrfmiddlewaretoken": CSRFtoken
	}).done(function(data) {
	    btn = $("#btn-save");
	    show_tooltip(btn, data.success, "Saved service", "Saving error. \n " + data.message);
	});
}

/* Watch a service */
function watch_services(detail_info) {
	var service = detail_info.dataset.name;
	var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
	$.post("watch", {
		services: [service],
		csrfmiddlewaretoken: CSRFtoken
	}).done(function(data) {
		btn = $("#btn-watch");
		if (data.success) {
			toggle_watch_button(btn[0], '1', "watch service", "unwatch service");
		}
		show_tooltip(btn, data.success, "Watching service.", "Watching failed. \n " + data.message);
	});
}

/* Unwatch a service */
function unwatch_services(detail_info) {
	var service = detail_info.dataset.name;
	var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
	$.post("unwatch", {
		services: [service],
		csrfmiddlewaretoken: CSRFtoken
	}).done(function(data) {
		btn = $("#btn-watch");
		if (data.success) {
			toggle_watch_button(btn[0], '0', "watch service", "unwatch service");
		}
		show_tooltip(btn, data.success, "Unwatched service.", "Unwatching not successful.");
	});
}

/* Run a service */
function run_services(detail_info) {
	var service = detail_info.dataset.name;
	var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
	$.post("start_services", {
		services: [service],
		csrfmiddlewaretoken: CSRFtoken
	}).done(function(data) {
		btn = $("#btn-run");
		if (data.success) {
			toggle_run_button(btn[0], '1', "start service", "stop service");
		}
		show_tooltip(btn, data.success, "Started service successfully.", "Failed to start service. \n " + data.message);
	});
}

/* Stop a service */
function stop_services(detail_info) {
	var service = detail_info.dataset.name;
	var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
	$.post("stop_services", {
		services: [service],
		csrfmiddlewaretoken: CSRFtoken
	}).done(function(data) {
		btn = $("#btn-run");
		if (data.success) {
			toggle_run_button(btn[0], '0', "start service", "stop service");
		}
		show_tooltip(btn, data.success, "Stopped service successfully.", "Failed to stop service. \n " + data.message);
	});
}

/* Sets the status of the run/stop and watch/unwatch buttons depending on
    the state of the service on the ROXcomposer server */
function set_buttons(detail_info) {
	var service = detail_info.dataset.name;
	set_run_button(service);
	set_watch_button(service);
}

/* Sets the status of the run/stop button depending on
    the state of the service on the ROXcomposer server */
function set_run_button(service) {
	var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
	$.post("check_running", {
		services: [service],
		csrfmiddlewaretoken: CSRFtoken
	}).done(function(data) {
		var running = "0";
		if (data.data[service] == true) {
			running = "1";
		}
		toggle_run_button($("#btn-run")[0], running, "start service", "stop service");
	});
}

/* Sets the status of the watch/unwatch button depending on
    the state of the service on the ROXcomposer server */
function set_watch_button(service) {
	var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
	$.post("check_watched", {
		services: [service],
		csrfmiddlewaretoken: CSRFtoken
	}).done(function(data) {
		var watched = "0";
		if (data.data[service] == true) {
			watched = "1";
		}
		toggle_watch_button($("#btn-watch")[0], watched, "watch service", "unwatch service");
	});
}
