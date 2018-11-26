function addToPipe(elem) {
    var selected_service = elem.dataset.value_name;
    var ul = document.getElementById("piped_service_list");
    var li = document.createElement("li");
    li.setAttribute("id", "{{ name }}");
    li.setAttribute("onclick", "removeFromPipe(this)");
    li.setAttribute("data-value_name", "{{ name }}");
    li.setAttribute("class", "list-group-item");
    li.appendChild(document.createTextNode(selected_service));
    ul.appendChild(li);
}

function removeFromPipe(elem){
    var selected_service = elem.dataset.value_name;
    var item = document.getElementById(selected_service);
    item.parentNode.removeChild(item);
}

function refresh() {
    setTimeout(function () {
        location.reload()
    }, 100);
}

function postPipeOptions() {
    var pipeline_name = document.getElementById("pipe_name").value;
    var pipeline_services = new Array();
    var pipelines = document.querySelectorAll('#piped_service_list li');
    for (i = 0; i < pipelines.length; i++) {
        pipeline_services.push(pipelines[i].innerHTML);
    }
    console.log(pipeline_services);
    var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
    $.post("create_pipeline", {name: pipeline_name, services: pipeline_services, csrfmiddlewaretoken: CSRFtoken}).done(function(){ location.reload(); });
}

function watch(elem){
    if(elem.getAttribute("aria-pressed") == 'true'){
        unwatch(elem);
    } else{
        console.log("Here")
        var selected_service = elem.dataset.value_name;
        var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
        if(selected_service){
            $.post("watch", {services: selected_service, csrfmiddlewaretoken : CSRFtoken}).done(function(){
            location.reload();
         });
        }

    }
}

function unwatch(elem){
    var selected_service = elem.dataset.value_name;
    var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
    if(selected_service){
        $.post("unwatch", {services: selected_service, csrfmiddlewaretoken : CSRFtoken}).done(function(){
        location.reload();
     });
    }
}

function run_service(elem){
    var selected_service = elem.dataset.value_name;
    var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
    $.post("start_service", {available_service_names:  [selected_service], csrfmiddlewaretoken : CSRFtoken}).done(function(){
        location.reload(); });

}

function stop_service(elem){
    var selected_service = elem.dataset.value_name;
    var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
    $.post("stop_service", {running_service_names:  [selected_service], csrfmiddlewaretoken : CSRFtoken}).done(function(){
        location.reload(); });
}

function show_pipeline(elem){
    var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
    var selected_pipe = elem.dataset.value_name;
    var selected_pipe_services = elem.dataset.value_services;
    var selected_active = elem.dataset.value_active;
    $.post("select_pipeline", {pipe_name: selected_pipe, pipe_services: selected_pipe_services, selected_active: selected_active, csrfmiddlewaretoken: CSRFtoken}).done(function(){ location.reload(); });

}