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