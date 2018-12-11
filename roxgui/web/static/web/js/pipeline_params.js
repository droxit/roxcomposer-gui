function create_pipeline_service_li_element(text_content) {
	// Top list element.
	var li = document.createElement("li");
	li.setAttribute("id", text_content);
	li.setAttribute("data-name", text_content);
	li.setAttribute("class", "list-group-item");

	var div0 = document.createElement("div");
	div0.className = "d-flex";
	var div1 = document.createElement("div");
	div1.className = "col-mb-9";
	var div2 = document.createElement("div");
	div2.className = "ml-auto";
	li.appendChild(div0);
	div0.appendChild(div1);
	div0.appendChild(div2);

	// Append service name.
	div1.appendChild(document.createTextNode(text_content));
	// Append button with icon.
	var button = document.createElement("button");
	button.setAttribute("type", "button");
	button.setAttribute("onclick", "remove_from_current_pipe(this)");
	button.setAttribute("data-name", text_content);
	button.setAttribute("class", "btn btn-default");
	button.setAttribute("data-toggle", "button");
	button.setAttribute("aria-pressed", "false");
	var icon = document.createElement("span");
	icon.setAttribute("class", "fas fa-trash-alt");
	button.appendChild(icon);
	div2.appendChild(button);
	return li;
}

function add_service_to_current_pipe(service_name) {
	var ul = document.getElementById("piped_service_list");
	var li = create_pipeline_service_li_element(service_name);
	ul.appendChild(li);
}

function add_to_current_pipe(elem) {
	var selected_service = elem.dataset.name;
	add_service_to_current_pipe(selected_service);
	write_active_pipeline_to_cookie();
}

function remove_from_current_pipe(elem) {
	var selected_service = elem.dataset.name;
	var item = document.getElementById(selected_service);
	item.parentNode.removeChild(item);
	write_active_pipeline_to_cookies();
}

function show_pipeline(elem) {
	// Get data from template.
	var selected_pipe = elem.dataset.name;
	var selected_pipe_services = $(elem).data("services");
	var selected_active = elem.dataset.active;
	// Convert pipeline services string to array.
	// Update pipeline name in corresponding text input.
	document.getElementById("pipe_name").value = selected_pipe;
	// Get list of services and remove all items.
	var ul = document.getElementById("piped_service_list");
	while (ul.firstChild) {
		ul.removeChild(ul.firstChild);
	}
	// Add new items to service list.
	for (i = 0; i < selected_pipe_services.length; i++) {
		var li = create_pipeline_service_li_element(selected_pipe_services[i]);
		ul.appendChild(li);
	}
	write_active_pipeline_to_cookies();
}

function create_or_update_pipeline() {
	var pipeline_name = document.getElementById("pipe_name").value;
	var pipeline_services = new Array();
	var pipelines = document.querySelectorAll('#piped_service_list li');
	for (i = 0; i < pipelines.length; i++) {
		pipeline_services.push(pipelines[i].innerText);
	}
	var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
	$.post("create_pipeline", {
		name: pipeline_name,
		services: pipeline_services,
		csrfmiddlewaretoken: CSRFtoken
	}).done(function() {
		location.reload();
	});
}

function post_message_to_pipeline() {
	var pipeline_name = document.getElementById("pipe_name").value;
	var message = document.getElementById("pipe_message_text").value;
	var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
	$.post("post_to_pipeline", {
		pipe_name: pipeline_name,
		pipe_message_text: message,
		csrfmiddlewaretoken: CSRFtoken
	});
}

function read_active_pipeline_from_cookies() {
    // Get cookies.
    var cookies = document.cookie.split(';');
    // Extract pipeline name as string.
    var pipeline_name = cookies[1].split("=")[1];
    // Extract list of pipeline services as string.
    var ps = cookies[2].split("=")[1];
    // Convert to real array.
    var pipeline_services = JSON.parse(ps);
    // Restore pipeline name.
    document.getElementById("pipe_name").value = pipeline_name;
    // Restore services in pipeline.
    for (var i = 0; i < pipeline_services.length; i++) {
        add_service_to_current_pipe(pipeline_services[i]);
    }
}

function write_active_pipeline_to_cookies() {
    // Write current pipeline name to cookie.
	var pipeline_name = document.getElementById("pipe_name").value;
	document.cookie = "pipeline_name_cookie=" + pipeline_name;
	// Write current services in pipeline to cookie.
	var pipeline_services = new Array();
	var pipelines = document.querySelectorAll('#piped_service_list li');
	for (i = 0; i < pipelines.length; i++) {
		pipeline_services.push(pipelines[i].innerText);
	}
    var json_str = JSON.stringify(pipeline_services);
    document.cookie = "pipeline_services_cookie=" + json_str;
}