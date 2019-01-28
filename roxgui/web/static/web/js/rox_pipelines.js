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
    dataset.services = JSON.parse(elem.dataset.title).services;
}


function create_pipe_detail(pipeline){
    var detail_container = document.createElement("div");
    detail_container.setAttribute("class", "container");

    var empty_row = document.createElement("div");
    empty_row.setAttribute("class", "row");
    var empty_col = document.createElement("div");
    empty_col.setAttribute("class", "col-md-12");
    empty_col.appendChild(document.createElement("p"));
    empty_row.appendChild(empty_col);
    detail_container.appendChild(empty_row);

    return detail_container;

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
