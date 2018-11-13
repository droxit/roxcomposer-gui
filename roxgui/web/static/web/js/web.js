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

function watch(){
    var options = $('#running_service_list').val();
    console.log(options)
    var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
    if(options.length >= 1){
        $.post("watch", {services: options, csrfmiddlewaretoken : CSRFtoken}).done(function(){
        location.reload();
     });
    }
}

function unwatch(){
    var options = $('#running_service_list').val();
    var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
    if(options.length >= 1){
        $.post("unwatch", {services: options, csrfmiddlewaretoken : CSRFtoken}).done(function(){
        location.reload();
     });
    }
}