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

function postPipeOptions(){
    var options = $('#piped_service_list option');

    var values = $.map(options ,function(option) {
        return option.value;
    });
    console.log(values);

    var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();

    $.post("create_pipeline", {services: values, csrfmiddlewaretoken : CSRFtoken}).done(function(){
        location.reload();
     });
}