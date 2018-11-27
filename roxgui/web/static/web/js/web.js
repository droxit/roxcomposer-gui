function create_pipeline_service_li_element(text_content){
    var li = document.createElement("li");
    li.setAttribute("id", "{{ name }}");
    li.setAttribute("onclick", "remove_from_current_pipe(this)");
    li.setAttribute("data-name", "{{ name }}");
    li.setAttribute("class", "list-group-item");
    li.appendChild(document.createTextNode(text_content));
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
    $.post("post_to_pipeline", {pipe_name: pipeline_name, pipe_message_text: message, csrfmiddlewaretoken: CSRFtoken}).done(function(){ location.reload(); });
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

function run_service(elem){
    var selected_service = elem.dataset.value_name;
    var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
    $.post("start_service", {available_service_names:  [selected_service], csrfmiddlewaretoken : CSRFtoken}).done(function(){
        location.reload(); });

}

function stop_service(elem){
    var selected_service = elem.dataset.name;
    var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
    $.post("stop_service", {running_service_names:  [selected_service], csrfmiddlewaretoken : CSRFtoken}).done(function(){
        location.reload(); });
}