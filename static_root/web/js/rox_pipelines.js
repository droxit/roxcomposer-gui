/*
#
# Define the dynamic pipeline functionality of the pipeline view.
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

/* Creates an empty detail view with the specific pipeline headline */
function show_empty_detail_view() {
	$("#data_detail_list").html("");
	var detail_headline = $("#headline_detail");
	detail_headline[0].setAttribute("onclick", "");

	detail_headline.html("<h4>Select a pipeline.</h4>");
}

/* Set the tooltips for all pipeline view buttons*/
function set_pipe_tooltips() {
	set_pipe_tooltip($("#btn-edit")[0].dataset, "edit name");
	set_pipe_tooltip($("#btn-delete")[0].dataset, "delete pipe");
	set_pipe_tooltip($("#btn-save")[0].dataset, "save changes");
	set_pipe_tooltip($("#btn-add")[0].dataset, "add new pipe");
	set_pipe_tooltip($("#btn-add-service")[0].dataset, "add new service to pipeline");
	set_pipe_tooltip($("#btn-send-msg")[0].dataset, "send");
	set_pipe_tooltip($("#btn-attach")[0].dataset, "attach a file");
	set_pipe_tooltip($("#btn-load-session")[0].dataset, "load a session");
	set_pipe_tooltip($("#btn-save-session")[0].dataset, "save a session");

}

/* Set the tooltip for a single button, the status is set to 0 and indicates if the pipe is running */
function set_pipe_tooltip(btn, tooltip) {
	btn.status = "0";
	set_tooltip(btn, tooltip);
}

/* Remove the 'disabled' status of those buttons that already have functionality */
function enable_detail_elements() {
	//"btn-watch" ,"btn-delete", "btn-save"
	["btn-edit", "btn-add-service", "btn-send-msg", "btn-save", "btn-delete"].forEach(function(btn) {
		btn_remove_disabled(btn);
	});
}

/* Remove the 'disabled' status of a single button */
function btn_remove_disabled(btn) {
	var btnedit = $("#" + btn + "")[0];
	btnedit.classList.remove("disabled");
}

/* Retrieve the dataset of the hidden 'detail info' element that contains information on callback functions and the selected pipe */
function get_dataset() {
	return $("#detail_info")[0].dataset;
}

/* Set the data for the dataset of the hidden 'detail info' element, which concerns the
    pipe name of the selected pipeline, and the services it contains */
function set_pipe_info(elem) {
	var dataset = get_dataset();
	var pipe = elem.dataset.name;
	dataset.name = pipe;
	dataset.services = JSON.stringify(JSON.parse(elem.dataset.title).services);
}

/* Adds a search bar for searching through available services below the selected pipe detail view.
    The search bar is at first disabled (not clickable) until the user selects a pipe. */
function add_search_bar() {
	var search_container = $("#search-bar-container");
	var search_btn_container = $("#search-btn-container");
	var searchbar = $("<input id='search_services' class='form-control' type='text'  list='data-service-list' placeholder='Add service ...' disabled='disabled'></input>");
	var service_datalist = $("<datalist id='data-service-list'></datalist>");
	var add_btn = $("<button type='button' id='btn-add-service' class='btn btn-primary btn-circle-big disabled' style='margin-left:-20px' onclick='add_service_to_pipe()'><span class='fas fa-plus'></span></button>")

    searchbar[0].addEventListener("keyup", function(event) {
		// Cancel the default action, if needed
		event.preventDefault();
		// When enter is pressed send the message to current pipe
		if (event.keyCode === 13) {
			add_btn[0].click();
		}
	});

	search_container.append(searchbar);
	search_container.append(service_datalist);
	search_btn_container.append(add_btn);

}

/* adds a disabled */
function add_send_message_and_session_restore() {
	var search_container = $("#content-container");
	var msg_row = $("<div class='row' style='margin-top:20px;margin-bottom:20px'></div>");
	var msg_col = $("<div class='col-md-5'></div>");
	var btn_col = $("<div class='col-md-2'></div>");
	var ssn_col = $("<div class='col-md-5 float-right'></div>");
	var ssn_float_right = $("<div class='float-right'></div>");

	msg_row.append(msg_col);
	msg_row.append(btn_col);
	msg_row.append(ssn_col);
	search_container.append(msg_row);

	var msg_input = $("<input id='send_msg' class='form-control' type='text' placeholder='Send a message to pipeline' disabled = 'disabled'></input>");
	msg_col.append(msg_input);


	var msg_send_btn = $("<button type='button' id='btn-send-msg' class='btn btn-primary btn-circle-big disabled' style='margin-left:-20px' onclick='send_msg_to_pipe()'><span class='fas fa-paper-plane'></span></button>");
	var attach_btn = $("<button type='button' id='btn-attach' class='btn btn-primary btn-circle-big disabled ' style='margin-left:10px' ><span class='fas fa-paperclip'></span></button>");
	btn_col.append(msg_send_btn);
	btn_col.append(attach_btn);

	var ssn_save_btn = $("<button type='button' id='btn-save-session' class='btn btn-secondary btn-circle-big ' \
	                        style='margin-left:-20px' onclick='save_session()'> \
	                        <span class='fas fa-download' aria-hidden='true'> \
	                        </span> \
	                        </button>");

    var ssn_load_btn = $("<button type='button' id='btn-load-session' class='btn btn-secondary btn-circle-big ' \
	                        style='margin-left: 10px' onclick='$(\"#load_session\").click()'> \
	                        <label for='load_session'> \
	                        <span class='fas fa-upload' aria-hidden='true'></span> \
	                        </label> \
	                        </button>");
    var ssn_load_input = $("<input type='file' id='load_session' style='display:none'>");
    ssn_load_btn.append(ssn_load_input);


    ssn_col.append(ssn_float_right);
    ssn_float_right.append(ssn_save_btn);
    ssn_float_right.append(ssn_load_btn);

    ssn_load_input[0].addEventListener("change", load_session, false);



	bind_message_enter(); //bind the enter key on the input field to send a message


}

/* binds the enter key on the send message input field to click the send button */
function bind_message_enter() {
	var msg_input = document.getElementById("send_msg");

	msg_input.addEventListener("keyup", function(event) {
		// Cancel the default action, if needed
		event.preventDefault();
		// When enter is pressed send the message to current pipe
		if (event.keyCode === 13) {
			document.getElementById("btn-send-msg").click();
		}
	});
}

/* Remove the disabled status of the send message input field */
function enable_send_msg() {
	var send_msg = $("#send_msg")[0];
	send_msg.disabled = '';

}

/* Remove the disabled status of the search bar so the user can search services and add them */
function enable_search_bar() {
	var searchbar = $("#search_services")[0];
	searchbar.disabled = '';
}


/* Downloads the current session */
function save_session(){
    var href = window.location + "/save_session";
    window.location = href;
}

/* Opens a dialog that asks from where the user wants to load the session */
function load_session(){
    var file = this.files[0];

    var reader = new FileReader();
    // Closure to capture the file information.
    reader.onload = (function (file) {
        return function (e) {
            try {
                session = JSON.parse(e.target.result);

                var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
                $.post("load_session", {
                    session: JSON.stringify(session),
                    csrfmiddlewaretoken: CSRFtoken,
                }).done(function(data) {
                    if(data.success){
                        location.reload();
                    }else{
                        show_tooltip($("#btn-load-session"), data.success, "Restored session", "Could not restore session: " + data.message);
                    }
                });
            } catch (ex) {
                show_tooltip($("#btn-load-session"), false, "", "Could not load session: " + ex);
            }
        }
    })(file);
    reader.readAsText(file);
}

/* Add a selected service to the currently viewed pipeline */
function add_service_to_pipe() {
	var searchbar = $('#search_services')[0];
	var pipe = $("#headline_detail")[0].dataset.name; // currently selected pipeline that is being edited
	var pipe_container = $("#services_in_pipeline")[0]; // the container where service cards will be added

	//Retrieve the selected service that is to be added to pipe (and its information)
	var selected_service = searchbar.value;
	var selected_service_info = $("#option_" + selected_service)[0].dataset.info;


	//Get the pipeline info
	var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
	$.post("get_pipeline_info", {
		pipe_name: pipe,
		csrfmiddlewaretoken: CSRFtoken,
	}).done(function(pipe_data) {
		//if the pipeline already exists
		if (jQuery.isEmptyObject(pipe_data.data)) {
			var current_services = []; //if it doesn't exist, create a new one
		} else {
			//Get the current service list of the pipeline
			var current_services = pipe_data.data.services;
		}
		//add the new service
		current_services.push({'service': selected_service});
        searchbar.value = '';

		//Update and save the new pipeline
		save_pipe_add_service(pipe, current_services, update_pipe)
	});
}

/* Remove the service that was clicked from current pipe. */
function remove_service_from_pipe(index) {
	var pipe = $("#headline_detail")[0].dataset.name; // currently selected pipeline that is being edited
	var pipe_container = $("#services_in_pipeline")[0]; // the container where service cards are


	//Get the pipeline info
	var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
	$.post("get_pipeline_info", {
		pipe_name: pipe,
		csrfmiddlewaretoken: CSRFtoken,
	}).done(function(pipe_data) {
		//if the pipeline already exists
		if (jQuery.isEmptyObject(pipe_data.data)) {
			var current_services = []; //if it doesn't exist, create a new one
		} else {
			//Get the current service list of the pipeline
			var current_services = pipe_data.data.services;
		}


		//remove the selected service
		if (index > -1) {
			current_services.splice(index, 1);
		}

		//Update and save the new pipeline
		save_pipe_add_service(pipe, current_services, update_pipe)
	});
}

/* update the detail view after an element has been changed in the pipe */
function update_pipe(pipe, services) {
	var pipe_info = $("#detail_info")[0].dataset;
	pipe_info.name = pipe;

	var new_detail = create_detail_view(pipe);
	add_detail_view(new_detail);
	add_data_entries_from_remote($('#search_field')[0], 'go_to_detail_view(this)', $('#data_info_list')[0], 'get_pipelines');
	//save_pipe_status()
}


/* When a pipeline has been selected this function is called to create the detail view containing the service cards
   of the selected pipeline */
function create_detail_view(pipeline) {

	//Create the container for the detail view
	var detail_container = document.createElement("div");
	detail_container.setAttribute("class", "container");
	detail_container.setAttribute("style", "padding:60px");

	var services_row = document.createElement("div");
	services_row.setAttribute("class", "row");

	var services_col = document.createElement("div");
	services_col.setAttribute("class", "col-md-12");
	services_row.appendChild(services_col);
	detail_container.appendChild(services_row);


	//Get the pipeline info
	var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
	$.post("get_pipeline_info", {
		pipe_name: pipeline,
		csrfmiddlewaretoken: CSRFtoken,
	}).done(function(pipe_data) {
	    // set the hiddel old pipeline name (in case of overwrite)
        $("#headline_detail")[0].dataset.old_name = pipeline

		//enable the searchbar and send message field so the user can edit the pipe and send messages
		enable_search_bar();
		enable_send_msg();
		var services_in_pipe = pipe_data.data.services;
		if (!services_in_pipe) {
			return;
		}
		$.post("get_service_info", {
			services: JSON.stringify(services_in_pipe),
			csrfmiddlewaretoken: CSRFtoken
		}).done(function(data) {

			var service_info = data;

			//remove this to view services next to each other
			var inner_container = document.createElement("div");
			inner_container.setAttribute("class", "container");
			inner_container.setAttribute("id", "services_in_pipeline");
			services_col.appendChild(inner_container);

			set_status_enabled();
			services_in_pipe.forEach(function(service) {
				var service_info_single = "";
				if (service_info[service["service"]]) {
					service_info_single = service_info[service["service"]];
				}
				add_service_card(service, service_info_single, inner_container);
			});
		});
	});
	return detail_container;

}


/* Adds a single service card to the services_container and sets the tooltip info to serviceinfo
   connecting lines between cards have not yet been implemented */
function add_service_card(service_obj, serviceinfo, services_container) {
    var service = service_obj["service"];
    var service_params = service_obj["parameters"];
	var prev = get_preceding_service(services_container);
	var i = services_container.childNodes.length;

	var newrow = document.createElement("div");
	newrow.setAttribute("class", "row");
	services_container.appendChild(newrow);

	//create the card for the current service
	var card = document.createElement("div");
	card.setAttribute("class", "card");
	card.classList.add("carddiv");
	card.setAttribute("style", "margin-bottom:30px; min-width:80%");
	newrow.appendChild(card);

	set_tooltip(card, convert_to_json_string(serviceinfo));

	var card_body = document.createElement("div");
	card_body.setAttribute("class", "card-body");
	card.appendChild(card_body);

	var card_header_container = document.createElement("div");
	card_header_container.setAttribute("class", "d-flex");
	card_body.appendChild(card_header_container);

	var card_header = document.createElement("div");
	card_header.setAttribute("class", "row ml-auto");
	card_header.setAttribute("style", "margin-top: -18px; margin-bottom:10px");
	card_header_container.appendChild(card_header);

	var btn_watch = document.createElement("button");
	btn_watch.setAttribute("style", "margin-right:5px");
	btn_watch.setAttribute("id", "btn-watch-" + i);
	btn_watch.setAttribute("data-toggle", "tooltip");
	btn_watch.setAttribute("data-placement", "top");
	btn_watch.setAttribute("data-name", service);
	btn_watch.setAttribute("data-status", "0");
	btn_watch.setAttribute("class", "btn btn-secondary btn-watch btn-circle btn-mini");
	btn_watch.setAttribute("onclick", "toggle_services(['" + service + "','" + btn_watch.id + "'],this, watch_services, unwatch_services)");

	set_watch_button(btn_watch); // update this buttons status (is the service being watched?)

	var btn_run = document.createElement("button");
	btn_run.setAttribute("style", "margin-right:5px");
	btn_run.setAttribute("id", "btn-run-" + i);
	btn_run.setAttribute("data-toggle", "tooltip");
	btn_run.setAttribute("data-placement", "top");
	btn_run.setAttribute("data-name", service);
	btn_run.setAttribute("data-status", "0");
	//btn_run.setAttribute("data-original-title", "run/start");
	btn_run.setAttribute("class", "btn btn-secondary btn-run btn-circle");
	btn_run.setAttribute("onclick", "toggle_services(['" + service + "','" + btn_run.id + "'],this, run_services, stop_services)");

	set_run_button(btn_run); // update this buttons status (is the service running?)

	card_header.appendChild(btn_run);
	card_header.appendChild(btn_watch);
	var btn_del = document.createElement("button");
	card_header.appendChild(btn_del);

	btn_del.setAttribute("class", "btn btn-secondary btn-circle");
	btn_del.setAttribute("style", "margin-right:5px");
    btn_del.setAttribute("id", "btn-del-" + i);
	btn_del.setAttribute("data-toggle", "tooltip");
	btn_del.setAttribute("data-placement", "top");
	btn_del.setAttribute("data-title", "delete from pipe");
	btn_del.setAttribute("onclick", "remove_service_from_pipe(" + i + ")")

	var btn_watch_img = document.createElement("span");
	var btn_del_img = document.createElement("span");
	var btn_run_img = document.createElement("span");
	btn_watch_img.setAttribute("class", "fas fa-xs fa-eye");
	btn_run_img.setAttribute("class", "fas fa-xs fa-play");
	btn_del_img.setAttribute("class", "fas fa-xs fa-times");
	btn_watch.appendChild(btn_watch_img);
	btn_del.appendChild(btn_del_img);
	btn_run.appendChild(btn_run_img);

	var card_text = document.createElement("p");
	card_text.setAttribute("class", "card-text");
	card_body.appendChild(card_text);

	card_text.appendChild(document.createTextNode(service));

	var card_footer = document.createElement("div");
	card_footer.setAttribute("class", "card-footer");
	card.appendChild(card_footer);

	var pipeline_param_container = document.createElement("div");
	pipeline_param_container.setAttribute("id", "pipeline_param_container");

	var plus_btn = document.createElement("button");
	plus_btn.setAttribute("style", "margin-right:5px");
	plus_btn.setAttribute("class", "btn btn-primary btn-circle");
	plus_btn.onclick = () => append_pipeline_param(pipeline_param_container, "custom parameter");
	var plus_span = document.createElement("span");
	plus_span.setAttribute("class", "fas fa-xs fa-plus")
	plus_btn.appendChild(plus_span);

	var minus_btn = document.createElement("button");
	minus_btn.setAttribute("class", "btn btn-primary btn-circle");
	minus_btn.onclick = () => delete_last_pipeline_param(pipeline_param_container);
	var minus_span = document.createElement("span");
	minus_span.setAttribute("class", "fas fa-xs fa-minus")
	minus_btn.appendChild(minus_span);

    // append all existing pipeline params to service card
	if(service_params){
	    service_params.forEach(function(param){
	        append_pipeline_param(pipeline_param_container, param);
	    });
	}

	card_footer.appendChild(plus_btn);
	card_footer.appendChild(minus_btn);
	card_footer.appendChild(pipeline_param_container);


}

function get_pipeline_params(param_container){
    var inputs = param_container.getElementsByTagName("input");
    var params = [];
    inputs.forEach(function(input){
        if(input.value)
            params.push(input.value);
    });
    return params;
}


/* Add editable value to pipeline service container. */
function append_pipeline_param(container, val) {
	var input = document.createElement("input");
	input.setAttribute("type", "text");
	input.setAttribute("class", "form-control")
	input.setAttribute("value", val);
	input.setAttribute("style", "margin-top:10px; min-width:160px")
	container.appendChild(input);
}

/* Delete last value from pipeline service container. */
function delete_last_pipeline_param(container) {
	var last_child = container.lastChild;
	container.removeChild(last_child);
}

/* This is supposed to return the card of the preceding service in the pipeline */
function get_preceding_service(container) {
	var node = container.lastElementChild;
	if (node) {
		if (node.classList.contains("card")) {
			return node;
		} else {
			return null;
		}
	} else {
		return null;
	}

}

/* Retrieve the new information (pipe name and service list) and create a new pipeline (or save/overwrite) */
function save_detail(elem) {
	if (check_disabled(elem)) {
		return;
	}
	var pipe_name = get_pipe_name();
	var services = get_services();
	$("#detail_info")[0].dataset.name = pipe_name;
	save_pipe(pipe_name, services, [$("#btn-save"), "Saved pipeline", "Saving the pipe failed. \n "]);

}

/* Overwrite an edited pipe on the roxcomposer after adding a service*/
function save_pipe_add_service(pipe, services) {
	save_pipe(pipe, services, [$("#btn-add-service"), "", "Adding service failed. \n "])
}


/* Save the pipeline as it currently is in the detail view. */
/*
function save_pipe_status(){
	var pipe_name = get_pipe_name();
	var services = get_services();
	save_pipe(pipe_name, services, [$("#btn-save"), "", ""])
}
*/


/* Retrieve the pipeline name  */
function get_pipe_name(){
    return  document.getElementById("headline_detail").lastElementChild.innerHTML;
}

/* Retrieve service list from detail view */
function get_services(){

    var service_cards = $("#services_in_pipeline")[0].querySelectorAll('.carddiv');
    //var service_cards = document.getElementById("services_in_pipe")
	var services = [];

	service_cards.forEach(function(card){
	    let service_json = {};
	    let service_name = card.getElementsByTagName("p")[0].innerHTML;
	    service_json["service"] = service_name;
	    let param_inputs = card.querySelectorAll('.form-control');
	    if(param_inputs.length){
	        service_json["parameters"] = [];
	        param_inputs.forEach(function(param_input){
	            if(param_input.value){
	                service_json["parameters"].push(param_input.value);
	            } else if(param_input.placeholder){
	                service_json["parameters"].push(param_input.placeholder);
	            }
	        });
	    }
		services.push(service_json);
	});
	return services
}

/* Create and save (or overwrite if name already exists) the new pipe on the roxcomposer. */
function save_pipe(pipe, services, tooltip_info) {
	var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
	$.post("create_pipeline", {
		services: JSON.stringify(services),
		pipe_name: pipe,
		csrfmiddlewaretoken: CSRFtoken
	}).done(function(data) {
		if (data.success) {
			update_pipe(pipe, services);

			//check if the pipe name has been change, if yes delete the old pipeline (overwrite)
			var old_name = $("#headline_detail")[0].dataset.old_name;
            if(old_name){
                if(old_name != pipe){
                    delete_pipeline(old_name);
                }
            }
	    }
	    show_tooltip(tooltip_info[0], data.success, tooltip_info[1], tooltip_info[2] + data.message)
	});
}

/* Create a modal popup to ask the user if they really want to delete a service. */
function delete_this(elem) {
    // save_pipe_status()
	var pipe_name = document.getElementById("headline_detail").lastElementChild.innerHTML;

	var popup_warning = $("<div class='modal' tabindex='-1' role='dialog'> \
  <div class='modal-dialog' role='document'> \
    <div class='modal-content'> \
      <div class='modal-header'> \
        <h5 class='modal-title'>Delete " + pipe_name + "?</h5> \
        <button type='button' class='close' data-dismiss='modal' aria-label='Close'> \
          <span aria-hidden='true'>&times;</span> \
        </button> \
      </div> \
      <div class='modal-body'> \
        <p>Are you sure you want to delete this pipeline?</p> \
      </div> \
      <div class='modal-footer'> \
        <button type='button' class='btn btn-primary' onclick='delete_pipeline(\"" + pipe_name + "\")'>Delete</button> \
        <button type='button' class='btn btn-secondary' data-dismiss='modal'>Close</button> \
      </div> \
    </div> \
  </div> \
</div>");

	popup_warning.modal("toggle");

}

/* Delete this pipeline on the ROXcomposer if it exists. */
function delete_pipeline(pipe) {
    var elem = $("#btn-delete")
	var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
	$.post("delete_pipeline", {
		pipe_name: pipe,
		csrfmiddlewaretoken: CSRFtoken
	}).done(function(data) {
		if (data.success) {
			location.reload();
	    }
		show_tooltip(elem, data.success, "", "Deleting pipeline failed. \n " + data.message);
	});
}


/* This is called when the user clicks the 'add new' button, it opens an empty detail view and
    sets the pipeline name to 'new pipe'. */
function add_new(elem) {
	if (check_disabled(elem)) {
		return;
	}
	go_to_new_detail_view("new pipe")
}

/* Send a message to the currently selected pipeline and show tooltip after */
function send_msg_to_pipe() {
	// Retrieve the info on currently selected pipe and message
	var pipe = document.getElementById('headline_detail').dataset.name;
	var msg_input_field = $('#send_msg');
	var msg = msg_input_field[0].value;

	var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
	$.post("send_msg", {
		msg: msg,
		pipe: pipe,
		csrfmiddlewaretoken: CSRFtoken
	}).done(function(data) {

		show_tooltip(msg_input_field, data.success, "Sent message successfully.", "Sending failed. \n " + data.message);

	});
}

/* Watch a service and then update all the watch buttons in the pipeline detail view. */
function watch_services(info) {
	var service = info[0];
	var btn = info[1];
	var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
	$.post("watch", {
		services: [service],
		csrfmiddlewaretoken: CSRFtoken
	}).done(function(data) {
		if (data.success) {
			update_watch_buttons();
		}
		show_tooltip($("#" + btn), data.success, "Watching.", "Failed to watch service. \n " + data.message);
	});
}

/* Unwatch a service and then update all the watch buttons in the pipeline detail view. */
function unwatch_services(info) {
	var service = info[0];
	var btn = info[1];
	var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
	$.post("unwatch", {
		services: [service],
		csrfmiddlewaretoken: CSRFtoken
	}).done(function(data) {
		if (data.success) {
			update_watch_buttons();
		}
		show_tooltip($("#" + btn), data.success, "Unwatched.", "Failed to unwatch service. \n " + data.message);
	});
}

/* Start a service and then update all the watch buttons in the pipeline detail view. */
function run_services(info) {
	var service = info[0];
	var btn = info[1];
	var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
	$.post("start_services", {
		services: [service],
		csrfmiddlewaretoken: CSRFtoken
	}).done(function(data) {
		if (data.success) {
			update_run_buttons();
		}
		show_tooltip($("#" + btn), data.success, "Running.", "Failed to start service. \n " + data.message);
	});
}

/* Stop a service and then update all the watch buttons in the pipeline detail view. */
function stop_services(info) {
	var service = info[0];
	var btn = info[1];
	var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
	$.post("stop_services", {
		services: [service],
		csrfmiddlewaretoken: CSRFtoken
	}).done(function(data) {
		if (data.success) {
			update_run_buttons();
		}
		show_tooltip($("#" + btn), data.success, "Stopped.", "Failed to stop service. \n " + data.message);
	});
}

/* Update all the watch buttons of single service cards in the pipeline detail view. */
function update_watch_buttons() {
	var services = get_service_buttons(".btn-watch");
	services.forEach(function(btn) {
		set_watch_button(btn);
	});
}

/* Update all the start buttons of single service cards in the pipeline detail view. */
function update_run_buttons() {
	set_status_enabled();
	var services = get_service_buttons(".btn-run");
	services.forEach(function(btn) {
		set_run_button(btn);
	});
}

/* For a single watch button of a service card set the status. */
function set_watch_button(btn) {
	var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
	var service_name = btn.dataset.name;

	$.post("check_watched", {
		services: [service_name],
		csrfmiddlewaretoken: CSRFtoken
	}).done(function(data) {
		var watched = "0";
		if (data.data[service_name] == true) {
			watched = "1";
		}
		toggle_watch_button(btn, watched, "", "");
	});

}

/* For a single start button of a service card set the status. */
function set_run_button(btn) {
	var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
	var service_name = btn.dataset.name;

	$.post("check_running", {
		services: [service_name],
		csrfmiddlewaretoken: CSRFtoken
	}).done(function(data) {
		var running = "0";
		if (data.data[service_name] == true) {
			running = "1";
		} else {
			set_status_disabled()
		}

		toggle_run_button(btn, running, "", "");
	});

}

/* Retrieve all the buttons with a certain identifier (e.g. '.btn-watch' for all watch buttons) from the
    pipeline detail view. Careful though, the window needs to be loaded already or else the container
    won't be found. Using $(window).on('load',..) did not work. */
function get_service_buttons(identifier) {
	return $("#services_in_pipeline")[0].querySelectorAll(identifier);
}

/* Currently not used because  */
function set_buttons(detail_info) {
	//
}

/* Sets the detail headline status to inactive (and muted). */
function set_status_disabled() {
	var pipe_status_span = $("#headline_status");
	pipe_status_span.html("");
	pipe_status_span.append("inactive");
	pipe_status_span.attr("class", "form-text text-muted");
}

/* Sets the detail headline status to active (and unmuted). */
function set_status_enabled() {
	var pipe_status_span = $("#headline_status");
	pipe_status_span.html("");
	pipe_status_span.append("active");
	pipe_status_span.attr("class", "form-text");
}
