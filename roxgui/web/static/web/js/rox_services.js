/*
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

	set_detail_info("");
}

function set_detail_info(name) {
	$("#detail_info")[0].dataset.name = name;
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
	["btn-edit", "btn-run", "btn-watch", "btn-save", "btn-delete"].forEach(function(btn) {
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

	// Create buttons to add / delete key value pairs.
	var btn_row = document.createElement("div");
	btn_row.setAttribute("class", "d-flex justify-content-center");
	var plus_btn = document.createElement("button");
	plus_btn.setAttribute("class", "btn btn-primary btn-circle-big float-center");
	plus_btn.setAttribute("style", "margin-top:10px; margin-bottom:10px; margin-right:10px");
	plus_btn.setAttribute("id", "add-parameter")
	plus_btn.onclick = () => append_param(detail_container, "key", "value");
	var plus_span = document.createElement("span");
	plus_span.setAttribute("class", "fas fa-plus")
	plus_btn.appendChild(plus_span);
	btn_row.appendChild(plus_btn);
	var minus_btn = document.createElement("button");
	minus_btn.setAttribute("style", "margin-top:10px; margin-bottom:10px");
	minus_btn.setAttribute("class", "btn btn-primary btn-circle-big float-center");
	minus_btn.onclick = () => delete_last_param(detail_container);
	var minus_span = document.createElement("span");
	minus_span.setAttribute("class", "fas fa-minus")
	minus_btn.appendChild(minus_span);
	btn_row.appendChild(minus_btn);
	detail_container.appendChild(btn_row)

	var hidden_old_name = document.createElement("p"); // This is important for overwriting the service when the name changes
    hidden_old_name.dataset.name = "";
    hidden_old_name.id = "hidden_old_name";
    var search_bar_container = document.getElementById("search-bar-container");
    search_bar_container.html = "";
    search_bar_container.appendChild(hidden_old_name);

	set_status(service); // Set the 'status' span to running or not running

	if (service === "") {
		// Service name is not given, so create empty detail view.
		set_detail_headline("new service");
		get_empty_params(detail_container);
	} else {
		// Service name is given, so add corresponding parameters in detail view.
		get_params(detail_container, service);
	}

	return detail_container;
}

/* Add editable key value pair to service container. */
function append_param(container, key, val) {
	var row = document.createElement("div");
	row.setAttribute("class", "row");
	container.appendChild(row);

	var col1 = document.createElement("div");
	col1.setAttribute("class", "col-md-2");

	var col2 = document.createElement("div");
	col2.setAttribute("class", "col-md-1");

	var col3 = document.createElement("div");
	col3.setAttribute("class", "col-md-9");

	row.appendChild(col1);
	row.appendChild(col2);
	row.appendChild(col3);

	var param_field_key = create_param_field(key);
	if (val.length < 50) {
		var param_field_value = create_param_field(val);
	} else {
		var param_field_value = create_param_textarea(val);
	}
	col1.appendChild(param_field_key);
	col2.appendChild(document.createTextNode(" : "));
	col3.appendChild(param_field_value);
}

function delete_last_param(container) {
	var detail_container = document.querySelector("#detail-container");
	var last_child = detail_container.lastChild;
	if (last_child.children.length == 3) {
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

		var service_json = data[service];

		if (service_json.classpath) {
			var key = "classpath";
			var val = service_json.classpath;
			append_param(container, key, val);
		}

		var service_params = service_json.params;

		jQuery.each(service_params, function(i, val) {
			if (i == "name") {
				var hidden_old_name = document.getElementById("hidden_old_name");
				hidden_old_name.dataset.name = val;
				return true;
			}
			if (typeof val === 'string' || val instanceof String) {
				value = val;
			} else {
				value = escapeHtml(convert_to_json_string(val));
			}
			append_param(container, i, value);
		});
	});
}

/* Add default parameter for new service to container. */
function get_empty_params(container) {
	append_param(container, "classpath", "new classpath");
	append_param(container, "ip", "new ip");
	append_param(container, "port", "new port");
}

/* Get all key-value pairs provided in current container and use them to create a new service. */
function save_detail(elem) {
	if (check_disabled(elem)) {
		return;
	}

	// Get detail container.
	var detail_container = document.querySelector("#detail-container");
	var service_name = document.querySelector("#headline_detail").dataset.name;
	// Iterate through its child nodes, each
	// containing a single key value pair.
	classpath_value = null;
	ip_value = null;
	port_value = null;
	name_value = service_name;
	key_array = []
	value_array = []

	for (var i = 0; i < detail_container.childNodes.length; i++) {
		var child = detail_container.childNodes[i].children;
		if (child.length == 3) {
			key = child[0].firstChild.innerText;
			value = child[2].firstChild.innerText;
			if (key == "classpath") {
				classpath_value = value;
			} else if (key == "port") {
				port_value = value;
			} else if (key == "ip") {
				ip_value = value;
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
	    console.log(data);
	    // If the service name was edited and a new service was created delete the old service
	    var hidden_old_name = document.getElementById("hidden_old_name");
		var old_name = hidden_old_name.dataset.name;
		if(old_name != name_value){
		    delete_service(old_name);
		}

		btn = $("#btn-save");
		show_tooltip(btn, data.success, "Saved service", "Saving error. \n " + data.message);
		add_data_entries_from_remote($('#search_field')[0], 'go_to_detail_view(this)', $('#data_info_list')[0], 'get_services');
	});
}

/* This is called when the user clicks the 'add new' button, it opens an empty detail view and
    sets the pipeline name to 'new pipe'. */
function add_new(elem) {
	if (check_disabled(elem)) {
		return;
	}
	elem.dataset.name = "";
	go_to_detail_view(elem);
}


/* Create a modal popup to ask the user if they really want to delete a service. */
function delete_this(elem) {
	var service = $("#detail_info")[0].dataset.name;

	var popup_warning = $("<div class='modal' tabindex='-1' role='dialog'> \
  <div class='modal-dialog' role='document'> \
    <div class='modal-content'> \
      <div class='modal-header'> \
        <h5 class='modal-title'>Delete " + service + "?</h5> \
        <button type='button' class='close' data-dismiss='modal' aria-label='Close'> \
          <span aria-hidden='true'>&times;</span> \
        </button> \
      </div> \
      <div class='modal-body'> \
        <p>Are you sure you want to delete this service?</p> \
      </div> \
      <div class='modal-footer'> \
        <button type='button' class='btn btn-primary' onclick='delete_service(\"" + service + "\")'>Delete</button> \
        <button type='button' class='btn btn-secondary' data-dismiss='modal'>Close</button> \
      </div> \
    </div> \
  </div> \
</div>");

	popup_warning.modal("toggle");

}

/* Delete a service. */
function delete_service(service) {
	var elem = $("#btn-delete")[0]
	var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();

	$.post("delete_service", {
		service: service,
		csrfmiddlewaretoken: CSRFtoken
	}).done(function(data) {
		if (data.success) {
			location.reload();
		}
		show_tooltip(elem, data.success, "", "Deleting service failed. \n " + data.message);
	});
}

/* Add watch and run buttons to the service detail headline. */
function add_watch_and_run_buttons() {
	var button_container = $("#button_headline");
	var btn_watch = $("<button type='button' id='btn-watch' class='btn btn-primary btn-circle-big float-right space-right disabled' onclick='toggle_services($(\"#detail_info\")[0],this, watch_services, unwatch_services)'><span class='fas fa-eye'></span></button>");
	var btn_run = $("<button type='button' id='btn-run' class='btn btn-primary btn-circle-big float-right space-right disabled' onclick='toggle_services($(\"#detail_info\")[0],this, run_services, stop_services)'><span class='fas fa-play'></span></button>");

	button_container.append(btn_watch);
	button_container.append(btn_run);
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
			set_status(service);
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
			set_status(service);
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

/* Sets the status text in the detail headline. */
function set_status(service) {
	var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
	var service_status_span = $("#headline_status");
	$.post("check_running", {
		services: [service],
		csrfmiddlewaretoken: CSRFtoken
	}).done(function(data) {
		service_status_span.html("");
		if (data.data[service] == true) {
			service_status_span.append("running");
			service_status_span.attr("class", "form-text");
		} else {
			service_status_span.append("inactive");
			service_status_span.attr("class", "form-text text-muted");
		}
	});
}
