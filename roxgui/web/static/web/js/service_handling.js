function run_service(elem){
    var selected_service = elem.dataset.value_name;
    var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
    $.post("start_service", {available_service_names:  [selected_service], csrfmiddlewaretoken : CSRFtoken}).done(function(data){
        // if error show tooltip
         });

}

function stop_service(elem){
    var selected_service = elem.dataset.name;
    var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
    $.post("stop_service", {running_service_names:  [selected_service], csrfmiddlewaretoken : CSRFtoken}).done(function(data){
        // if error show tooltip
         });
}

function get_services(){
    var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
    $.post("get_services", {csrfmiddlewaretoken : CSRFtoken}).done(function(data){
        // update available and running services
         });
}

function update_running_services(win, services){

}

function update_available_services(win, services){}

function create_running_service_card(win, service){}

function remove_running_service_card(win, service){}

function create_available_service_card(win, service){}

function remove_available_service_card(win, service){}