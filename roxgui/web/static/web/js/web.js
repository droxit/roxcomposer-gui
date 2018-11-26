function addToPipe() {
    var selectedOpts = $('#running_service_list').val();
    if (selectedOpts.length >= 1) {
        for (var i = 0; i < selectedOpts.length; i++) {
            var opt = selectedOpts[i];
            $('#piped_service_list').append(new Option(opt, opt));
        }
    }
}

function removeFromPipe() {
    $('#piped_service_list').find('option:selected').remove()
}

function refresh() {
    setTimeout(function () {
        location.reload()
    }, 100);
}

function postPipeOptions() {
    var pipeline_options = $('#piped_service_list option');
    var pipeline_name = document.getElementById('pipeline_name').value;
    var pipeline_services = $.map(pipeline_options, function(option) {
        return option.value;
    });
    var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
    $.post("create_pipeline", {name: pipeline_name, services: pipeline_services, csrfmiddlewaretoken : CSRFtoken}).done(function(){
        location.reload();
     });
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
    var selected_pipe = elem.dataset.value_name;
    var selected_pipe_services = elem.dataset.value_services;
    var selected_active = elem.dataset.value_active;
    console.log(selected_active);
    var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
    $.post("select_pipeline", {pipe_name: selected_pipe, pipe_services: selected_pipe_services, selected_active:selected_active, csrfmiddlewaretoken : CSRFtoken}).done(function(){
        location.reload(); });
}

