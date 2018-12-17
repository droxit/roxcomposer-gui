// Execute on startup.
document.getElementById("pipe_name").addEventListener("change", write_active_pipeline_to_cookies);
document.getElementById("piped_service_list").addEventListener("click", write_active_pipeline_to_cookies);
document.getElementById("pipe_message_text").addEventListener("change", write_active_pipeline_to_cookies);
read_active_pipeline_from_cookies();


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
    write_active_pipeline_to_cookies();
}

function add_to_current_pipe(elem) {
	var selected_service = elem.dataset.name;
	add_service_to_current_pipe(selected_service);
}

function remove_from_current_pipe(elem) {
	var selected_service = elem.dataset.name;
	var item = document.getElementById(selected_service);
	item.parentNode.removeChild(item);
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
    var cookies = document.cookie.split('; ');
    // Restore cookie data (if possible).
    for (var i = 0; i < cookies.length; i++) {
        // Extract data.
        var cookie = cookies[i].split('=');
        var id = cookie[0];
        var val = cookie[1];
        // Write data to HTML template excluding CSRF token.
        if (id == 'pipe_name' || id == 'pipe_message_text') {
            document.getElementById(id).value = val;
        } else if (id == 'piped_service_list') {
            var ps = JSON.parse(val);
            for (var j = 0; j < ps.length; j++) {
                add_service_to_current_pipe(ps[j]);
            }
        }
    }
}

function write_active_pipeline_to_cookies() {
    // Write current pipeline name to cookie.
    // Use corresponding HTML ID tag as cookie name.
	var pipeline_name = document.getElementById('pipe_name').value;
	document.cookie = "pipe_name=" + pipeline_name;
	// Write current services in pipeline to cookie.
	var pipeline_services = new Array();
	var pipelines = document.querySelectorAll('#piped_service_list li');
	for (var i = 0; i < pipelines.length; i++) {
		pipeline_services.push(pipelines[i].innerText);
	}
    var json_str = JSON.stringify(pipeline_services);
    document.cookie = "piped_service_list=" + json_str;
    // Write current message text to cookie.
    var msg_text = document.getElementById('pipe_message_text').value;
    document.cookie = "pipe_message_text=" + msg_text
}