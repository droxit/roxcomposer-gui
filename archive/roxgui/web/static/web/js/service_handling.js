/*
# encoding: utf-8
#
# Define web views.
#
# devs@droxit.de
#
# Copyright (c) 2018 droxIT GmbH
#
*/

// Update services windows
get_services();

function run_service(elem) {
	var selected_service = elem.dataset.value_name;
	var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
	$.post("start_service", {
		available_service_names: [selected_service],
		csrfmiddlewaretoken: CSRFtoken
	}).done(function(data) {
		// TODO: if error show tooltip
		get_services();
	});

}

function stop_service(elem) {
	var selected_service = elem.dataset.name;
	var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
	$.post("stop_service", {
		running_service_names: [selected_service],
		csrfmiddlewaretoken: CSRFtoken
	}).done(function(data) {
		// TODO: if error show tooltip
		get_services();
	});
}

function get_services() { // update available and running services
	var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
	$.post("get_services", {
		csrfmiddlewaretoken: CSRFtoken
	}).done(function(data) {
		running_win = document.getElementById("running_services");
		available_win = document.getElementById("available_services");
		update_available_services(available_win, data.available_services);
		update_running_services(running_win, data.running_services, data.watch_active);
	});
}

function update_running_services(win, services, watch_status) {
	var service_ids = [];
	for (var service in services) { //for every service check if it is already running
		service_ids.push(service)
		var service_info = services[service];
		//check if service card already exists and create a new one if not
		if (document.getElementById("runservice-" + service) == null) {
			if (watch_status == null)
				update_watch_status(false);

			if (watch_status[service] != null) {
				create_running_service_card(win, service, service_info, watch_status[service]);
			} else {
				create_running_service_card(win, service, service_info, false);
			}
		}
	}
	// delete every service that was not in services list
	var services_cards = win.children;
	for (var i = 0; i < services_cards.length; i++) {
		if (services_cards[i].nodeType == 1) {
			var serv = services_cards[i];
			var serv_id = serv.id.substring(11, serv.id.length);
			if (!service_ids.includes(serv_id))
				serv.remove();
		}
	}
}

function update_available_services(win, services) {
	var service_ids = [];
	for (var service in services) { //for every service check if it is already in the list
		service_ids.push(service);
		var service_info = services[service];
		//check if service card already exists and create a new one if not
		if (document.getElementById("avservice-" + service) == null) {
			create_available_service_card(win, service, service_info);
		}
	}

	// delete every service that was not in services list
	var services_cards = win.children;
	for (var i = 0; i < services_cards.length; i++) {
		if (services_cards[i].nodeType == 1) {
			var serv = services_cards[i];
			var serv_id = serv.id.substring(10, serv.id.length);
			if (!service_ids.includes(serv_id) && serv.id != 'new_service')
				serv.remove();
		}
	}
}

function parse_service_info(service_info) {
    // Extract classpath as string.
    var classpath = service_info.classpath;
    // Extract parameters as string.
    var params = JSON.stringify(service_info.params);
    // Concatenate both strings.
    return classpath + "\n\n" + params;
}


function create_running_service_card(win, service, service_info, watch_active) {
	// Basic button.
	var btn = document.createElement("button");
	btn.setAttribute("type", "button");
	btn.setAttribute("data-name", service);
	btn.setAttribute("class", "btn btn-round float-right");
	btn.setAttribute("data-toggle", "button");

	// Button to add service to pipeline.
	var btn_down = btn.cloneNode();
	btn_down.setAttribute("onclick", "add_to_current_pipe(this)");
	btn_down.setAttribute("title", "Add service to current pipeline.");
	var spn_down = document.createElement("span");
	spn_down.setAttribute("class", "fas fa-arrow-down fa-xs");
	btn_down.appendChild(spn_down);

	// Button to watch / unwatch service.
	var btn_watch = btn.cloneNode();
	btn_watch.setAttribute("onclick", "watch(this)");
	btn_watch.setAttribute("id", "watch-button-" + service);
	var spn_watch = document.createElement("span");
	spn_watch.setAttribute("id", "watch-span-" + service);
	if (watch_active) {
		spn_watch.setAttribute("class", "fas fa-eye fa-xs");
		btn_watch.setAttribute("data-watched", "true");
		btn_watch.setAttribute("title", "Watch / unwatch service.");
	} else {
		spn_watch.setAttribute("class", "fas fa-eye-slash fa-xs");
		btn_watch.setAttribute("data-watched", "false");
		btn_watch.setAttribute("title", "Watch / unwatch service.");
	}
	btn_watch.appendChild(spn_watch);

	// Button to stop service.
	var btn_del = btn.cloneNode();
	btn_del.setAttribute("onclick", "stop_service(this)");
	btn_del.setAttribute("title", "Stop service.");
	var spn_del = document.createElement("span");
	spn_del.setAttribute("class", "fas fa-trash-alt fa-xs");
	btn_del.appendChild(spn_del);

	// Card header with buttons.
	var card_header = document.createElement("div");
	card_header.setAttribute("class", "card-header");
	card_header.appendChild(btn_del);
	card_header.appendChild(btn_watch);
	card_header.appendChild(btn_down);

	// Card body with service name.
	var card_body = document.createElement("div");
	card_body.setAttribute("class", "card-body");
	card_body.setAttribute("title", parse_service_info(service_info));
	card_body.appendChild(document.createTextNode(service));

	// Card with header and body.
	var card = document.createElement("div");
	card.setAttribute("class", "card");
	card.setAttribute("id", "runservice-" + service)
	card.appendChild(card_header);
	card.appendChild(card_body);

	// Add card to parent element.
	win.appendChild(card);
}

function create_available_service_card(win, service, service_info) {
	var li = document.createElement("li");
	li.setAttribute("id", "avservice-" + service);
	li.setAttribute("class", "list-group-item");
	li.setAttribute("onclick", "run_service(this)");
	li.setAttribute("data-value_name", service);
	li.setAttribute("title", parse_service_info(service_info));
	li.appendChild(document.createTextNode(service));
	win.appendChild(li);
}
