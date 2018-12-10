function watch(elem){
    if(elem.getAttribute("aria-pressed") == 'true'){
        unwatch(elem);
    } else{
        var selected_service = elem.dataset.name;
        var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
        if(selected_service){
            $.post("watch", {services: selected_service, csrfmiddlewaretoken : CSRFtoken}).done(function(data){
                //TODO: error handling/tooltips
                var spn = elem.getElementsByTagName('span')[0];
                update_watch_buttons();
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
            update_watch_buttons();
        });
    }
}

function update_watch_buttons(){
    var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
    $.post("get_watched_status", {csrfmiddlewaretoken : CSRFtoken}).done(function(watch_active){
        //get the running services
        var running_services = document.getElementById('running_services').children;
        for(var i in running_services) {
            if(running_services[i].nodeType == 1){
                var serv = running_services[i];
                var serv_id = serv.id.substring(11, serv.id.length);

                // update watch button for every service
                var spn = document.getElementById('watch-span-'+serv_id);
                if(watch_active[serv_id]){
                    spn.setAttribute("class", "fas fa-eye");
                }else{
                    spn.setAttribute("class", "fas fa-eye-slash");
                }
            }
        }
     });


}