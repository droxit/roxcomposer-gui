function show_empty_detail_view(){
    $("#data_detail_list").html("");
    var detail_headline = $("#headline_detail");

    detail_headline.html("<h4>Select a service.</h4>");
}


function set_service_tooltips(){
    set_service_tooltip($("#btn-watch")[0].dataset, "(un)watch service");
    set_service_tooltip($("#btn-edit")[0].dataset, "edit name");
    set_service_tooltip($("#btn-run")[0].dataset, "run/stop service");
    set_service_tooltip($("#btn-delete")[0].dataset, "delete service");
    set_service_tooltip($("#btn-save")[0].dataset, "save changes");
    set_service_tooltip($("#btn-add")[0].dataset, "add new service");
}

function set_service_tooltip(btn, tooltip){
    btn.status = "0";
    set_tooltip(btn, tooltip);
}

function enable_detail_headline_btns(){
    //"btn-watch" ,"btn-delete", "btn-save"
    ["btn-edit", "btn-run", "btn-watch"].forEach(function(btn){
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

function set_service_info(elem){
    var dataset = get_dataset();
    var service = elem.dataset.name;
    dataset.name = service;
    dataset.services = [elem.dataset.name];
    dataset.title = elem.dataset.title;
}

function create_service_detail(service){
    var detail_container = document.createElement("div");
    detail_container.setAttribute("class", "container");

    var empty_row = document.createElement("div");
    empty_row.setAttribute("class", "row");
    var empty_col = document.createElement("div");
    empty_col.setAttribute("class", "col-md-12");
    empty_col.appendChild(document.createElement("p"));
    empty_row.appendChild(empty_col);
    detail_container.appendChild(empty_row);


    var list_of_params = get_params(service);
    list_of_params.forEach(function(param_pair){

        var row = document.createElement("div");
        row.setAttribute("class", "row");
        detail_container.appendChild(row);

        var col1 = document.createElement("div");
        col1.setAttribute("class", "col-md-5");
        col1.setAttribute("align", "center");

        var col2 = document.createElement("div");
        col2.setAttribute("class", "col-md-1");
        col2.setAttribute("align", "center");

        var col3 = document.createElement("div");
        col3.setAttribute("class", "col-md-5");
        col3.setAttribute("align", "center");

        row.appendChild(col1);
        row.appendChild(col2);
        row.appendChild(col3);

        var param_field_key = create_param_field(param_pair[0]);
        var param_field_value = create_param_field(param_pair[1]);
        col1.appendChild(param_field_key);
        col2.appendChild(document.createTextNode(" : "));
        col3.appendChild(param_field_value);

    });

    var service_name = document.createTextNode(service.id);
    return detail_container;

}

function get_params(service){
    var json_params = JSON.parse(service.dataset.title);
    if(json_params.classpath){
        var param_arr = [["classpath", JSON.stringify(json_params.classpath, null, ' ')]];
    }
    if(json_params.path){
        var param_arr = [["path", JSON.stringify(json_params.path, null, ' ')]];
    }

    jQuery.each(json_params.params, function(i, val) {
        val = JSON.stringify(val, null, ' ');

        param_arr.push([i, val]);
    });
    return param_arr;
}

function save_service(service){
    //TODO
}

function watch_service(detail_info){
    var service = detail_info.dataset.name;
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

function unwatch_service(service){
    var service = detail_info.dataset.name;
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


function run_service(detail_info){
    var service = detail_info.dataset.name;
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

function stop_service(detail_info){
    var service = detail_info.dataset.name;
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


function set_service_buttons(detail_info){
    var service = detail_info.dataset.name;
    set_run_button(service);
    set_watch_button(service);
}

function set_run_button(service){
    var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
    $.post("check_running", {
		services: [service],
		csrfmiddlewaretoken: CSRFtoken
	}).done(function(data) {
	    var running = "0";
	    if(data.data[service] == true){
            running = "1";
	    }
	    toggle_run_button($("#btn-run")[0], running);
	});
}

function set_watch_button(service){
    var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
    $.post("check_watched", {
		services: [service],
		csrfmiddlewaretoken: CSRFtoken
	}).done(function(data) {
	    var watched = "0";
	    if(data.data[service] == true){
            watched = "1";
	    }
	    toggle_watch_button($("#btn-watch")[0], watched);
	});
}

