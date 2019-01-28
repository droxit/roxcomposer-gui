
function show_empty_detail_view(){
    $("#data_detail_list").html("");
    var detail_headline = $("#headline_detail");

    detail_headline.html("<h4>Select a pipeline.</h4>");
}


function set_pipe_tooltips(){
    set_pipe_tooltip($("#btn-watch")[0].dataset, "(un)watch all services in pipeline");
    set_pipe_tooltip($("#btn-edit")[0].dataset, "edit name");
    set_pipe_tooltip($("#btn-run")[0].dataset, "run/stop all services in pipe");
    set_pipe_tooltip($("#btn-delete")[0].dataset, "delete pipe");
    set_pipe_tooltip($("#btn-save")[0].dataset, "save changes");
    set_pipe_tooltip($("#btn-add")[0].dataset, "add new pipe");
}

function set_pipe_tooltip(btn, tooltip){
    btn.status = "0";
    btn.toggle = "tooltip";
    btn.placement = "bottom";
    btn.title = tooltip;
}


function enable_detail_headline_btns(){
    //"btn-watch" ,"btn-delete", "btn-save"
    ["btn-edit"].forEach(function(btn){
        btn_remove_disabled(btn);
    });
}

function btn_remove_disabled(btn){
    var btnedit = $("#"+btn+"")[0];
    btnedit.classList.remove("disabled");
}

function get_dataset(){
    return $("#detail_info")[0].dataset;
}

function set_pipe_info(elem){
    var dataset = get_dataset();
    var pipe = elem.dataset.name;
    dataset.name = pipe;
    dataset.services = JSON.stringify(JSON.parse(elem.dataset.title).services);
}


function create_pipe_detail(pipeline){
    var data = get_dataset()
    var detail_container = document.createElement("div");
    detail_container.setAttribute("class", "container");
    detail_container.setAttribute("style", "padding:60px");


    var services_in_pipe = JSON.parse(data.services);
    var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
	$.post("get_service_info", {
		services: services_in_pipe,
		csrfmiddlewaretoken: CSRFtoken
	}).done(function(data) {
	    var service_info = data.data;

        var services_row = document.createElement("div");
        services_row.setAttribute("class", "row");

        var services_col = document.createElement("div");
        services_col.setAttribute("class", "col-md-12");
        services_col.setAttribute("id", "services_in_pipe");
        services_row.appendChild(services_col);
        detail_container.appendChild(services_row);

        //remove this to view services next to each other
        var inner_container = document.createElement("div");
        inner_container.setAttribute("class", "container");
        services_col.appendChild(inner_container);

        services_in_pipe.forEach(function(service){
            var service_info_single = "";
            if(service_info[service]){
                service_info_single = service_info[service];
            }
            add_service_card(service, service_info_single, inner_container);
        });


	});

    return detail_container;

}

function add_service_card(service, serviceinfo, services_container){
    var prev = get_preceding_service(services_container);

    var newrow = document.createElement("div");
    newrow.setAttribute("class","row");
    services_container.appendChild(newrow);

    //create the card for the current service
    var card = document.createElement("div");
    card.setAttribute("class", "card");
    card.classList.add("carddiv");
    card.setAttribute("style", "width: min-content; margin-bottom:30px");
    newrow.appendChild(card);

    set_tooltip(card, serviceinfo);

    var card_body = document.createElement("div");
    card_body.setAttribute("class", "card-body");
    card.appendChild(card_body);

    var card_header_container = document.createElement("div");
    card_header_container.setAttribute("class", "d-flex");
    card_body.appendChild(card_header_container);

    var card_header = document.createElement("div");
    card_header.setAttribute("class", "row ml-auto");
    card_header.setAttribute("style", "margin-top: -30px;")
    card_header_container.appendChild(card_header);

    var btn_watch = document.createElement("button");
    btn_watch.setAttribute("style", "margin-right:5px");
    card_header.appendChild(btn_watch);
    var btn_del = document.createElement("button");
    card_header.appendChild(btn_del);

    btn_watch.setAttribute("class", "btn btn-secondary disabled btn-sm");
    btn_del.setAttribute("class", "btn btn-secondary disabled btn-sm");

    var btn_watch_img = document.createElement("span");
    var btn_del_img = document.createElement("span");
    btn_watch_img.setAttribute("class", "fas fa-eye");
    btn_del_img.setAttribute("class", "fas fa-trash");
    btn_watch.appendChild(btn_watch_img);
    btn_del.appendChild(btn_del_img);


    var card_text = document.createElement("p");
    card_text.setAttribute("class", "card-text");
    card_body.appendChild(card_text);

    card_text.appendChild(document.createTextNode(service));

    //create the connection line to the preceding service
    if(prev){
        //create connection
    }


}


function get_preceding_service(container){
    var node = container.lastElementChild;
    if(node){
            if(node.classList.contains("card")){
            return node;
        }else{
            return null;
        }
    }else{
        return null;
    }

}

function save_pipe(pipe){
    //TODO
}



function watch_pipe(detail_info){
    var services = detail_info.dataset.services;
    var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
	$.post("watch", {
		services: [service],
		csrfmiddlewaretoken: CSRFtoken
	}).done(function(data) {
	    btn = $("#btn-watch");
	    if(data.success){
	        toggle_watch_button(btn[0], '1', data.success);
	    }
		show_tooltip(btn, data.success, "Watching service.", "Watching failed. \n "+data.message);
	});
}

function unwatch_pipe(detail_info){
    var services = detail_info.dataset.services;
    var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
	$.post("unwatch", {
		services: [service],
		csrfmiddlewaretoken: CSRFtoken
	}).done(function(data) {
	    btn = $("#btn-watch");
	    if(data.success){
	        toggle_watch_button(btn[0], '0', data.success);
		}
		show_tooltip(btn, data.success, "Unwatched service.", "Unwatching not successful.");
	});
}


function run_pipe(detail_info){
    var services = detail_info.dataset.services;
    var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
	$.post("start_services", {
		services: [service],
		csrfmiddlewaretoken: CSRFtoken
	}).done(function(data) {
	    btn = $("#btn-run");
	    if(data.success){
	        toggle_run_button(btn[0], '1', data.success);
		}
		show_tooltip(btn, data.success, "Started service successfully.", "Failed to start service. \n "+data.message);
	});
}

function stop_pipe(detail_info){
    var services = detail_info.dataset.services;
    var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
	$.post("stop_services", {
		services: [service],
		csrfmiddlewaretoken: CSRFtoken
	}).done(function(data) {
	    btn = $("#btn-run");
	    if(data.success){
    	    toggle_run_button(btn[0], '0' , data.success);
		}
		show_tooltip(btn, data.success, "Stopped service successfully.", "Failed to stop service. \n "+data.message);
	});
}


//TODO
function set_pipe_buttons(detail_info){
    var pipe = detail_info.dataset.name;
    //set_pipe_run_button(pipe);
    //set_pipe_watch_button(pipe);
}

function set_pipe_run_button(pipe){
    var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
    $.post("check_running", {
		services: [services],
		csrfmiddlewaretoken: CSRFtoken
	}).done(function(data) {
	    var running = "0";
	    if(data.data[service] == true){
            running = "1";
	    }
	    toggle_run_button($("#btn-run")[0], running);
	});
}

function set_pipe_watch_button(pipe){
    var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
    $.post("check_watched", {
		services: [services],
		csrfmiddlewaretoken: CSRFtoken
	}).done(function(data) {
	    var watched = "0";
	    if(data.data[service] == true){
            watched = "1";
	    }
	    toggle_watch_button($("#btn-watch")[0], watched);
	});
}
