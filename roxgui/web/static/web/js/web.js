function create_pipeline_service_li_element(text_content){
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

function add_to_current_pipe(elem) {
    var selected_service = elem.dataset.name;
    var ul = document.getElementById("piped_service_list");
    var li = create_pipeline_service_li_element(selected_service);
    ul.appendChild(li);
}

function remove_from_current_pipe(elem){
    var selected_service = elem.dataset.name;
    var item = document.getElementById(selected_service);
    item.parentNode.removeChild(item);
}

function refresh() {
    setTimeout(function () { location.reload() }, 100);
}

function show_pipeline(elem){
    // Get data from template.
    var selected_pipe = elem.dataset.name;
    var selected_pipe_services = $(elem).data("services");
    var selected_active = elem.dataset.active;
    // Convert pipeline services string to array.
    // Update pipeline name in corresponding text input.
    document.getElementById("pipe_name").value = selected_pipe;
    // Get list of services and remove all items.
    var ul = document.getElementById("piped_service_list");
    while(ul.firstChild){
        ul.removeChild(ul.firstChild);
    }
    // Add new items to service list.
    for (i = 0; i < selected_pipe_services.length; i++) {
        var li = create_pipeline_service_li_element(selected_pipe_services[i]);
        ul.appendChild(li);
    }
}

function create_or_update_pipeline(){
    var pipeline_name = document.getElementById("pipe_name").value;
    var pipeline_services = new Array();
    var pipelines = document.querySelectorAll('#piped_service_list li');
    for (i = 0; i < pipelines.length; i++) {
        pipeline_services.push(pipelines[i].innerText);
    }
    var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
    $.post("create_pipeline", {name: pipeline_name, services: pipeline_services, csrfmiddlewaretoken: CSRFtoken}).done(function(){ location.reload(); });
}

function post_message_to_pipeline(){
    var pipeline_name = document.getElementById("pipe_name").value;
    var message = document.getElementById("pipe_message_text").value;
    var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
    $.post("post_to_pipeline", {pipe_name: pipeline_name, pipe_message_text: message, csrfmiddlewaretoken: CSRFtoken});
}

function watch(elem){
    if(elem.getAttribute("aria-pressed") == 'true'){
        unwatch(elem);
    } else{
        var selected_service = elem.dataset.name;
        var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
        if(selected_service){
            $.post("watch", {services: selected_service, csrfmiddlewaretoken : CSRFtoken}).done(function(){
                location.reload(); });
        }
    }
}

function unwatch(elem){
    var selected_service = elem.dataset.name;
    var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
    if(selected_service){
        $.post("unwatch", {services: selected_service, csrfmiddlewaretoken : CSRFtoken}).done(function(){
            location.reload(); });
    }
}

//This updates the constantly reloaded elements (messages, logs)
acc = document.getElementById("accordion");
log_win = document.getElementById("log");
setInterval(function() {
   get_msg_status(acc);
   update_log(log_win);
}, 100);