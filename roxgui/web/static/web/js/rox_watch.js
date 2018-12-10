function watch(elem){
    if(elem.dataset.watched == "true"){
        unwatch(elem);
    } else{
        var selected_service = elem.dataset.name;
        var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
        if(selected_service){
            $.post("watch", {services: selected_service, csrfmiddlewaretoken : CSRFtoken}).done(function(data){
                //TODO: error handling/tooltips
                update_watch_status(true);
             });
        }
    }
}

function unwatch(elem){
    var selected_service = elem.dataset.name;
    var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
    if(selected_service){
        $.post("unwatch", {services: selected_service, csrfmiddlewaretoken : CSRFtoken}).done(function(data){
            //TODO: error handling/tooltips
            update_watch_status(true);
        });
    }
}

function update_watch_buttons(){

    //get the running services
    var running_services = document.getElementById('running_services').children;
    for(var i in running_services) {
        if(running_services[i].nodeType == 1){
            var serv = running_services[i];
            var serv_id = serv.id.substring(11, serv.id.length);

            var btn = document.getElementById('watch-button-'+serv_id);

            // update watched status in card
            if(watch_active[serv_id] != null)
                btn.setAttribute("data-watched", watch_active[serv_id]);

            // update watch button for every service
            var spn = document.getElementById('watch-span-'+serv_id);
            if(watch_active[serv_id]){
                spn.setAttribute("class", "fas fa-eye");
            }else{
                spn.setAttribute("class", "fas fa-eye-slash");
            }
        }
    }


}

function update_watch_status(update_buttons){
    var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
    $.post("get_watched_status", {csrfmiddlewaretoken : CSRFtoken}).done(function(watch_active){
        console.log(watch_active)
        if(update_buttons)
            update_watch_buttons(watch_active);
     });
}