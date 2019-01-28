function create_headline(name){
    var detail_info = $("#detail_info")[0];
    detail_info.dataset.name = name;

    var headline = document.createElement("div");
    headline.setAttribute("id", "headline_detail");
    headline.setAttribute("onclick", "edit_detail_headline()");

    var header = document.createElement("h4");
    header.appendChild(document.createTextNode(name));
    headline.appendChild(header);
    return headline;
}

function set_detail_headline(val){
    var headline = $("#headline_detail");
    var new_headline = create_headline(val);
    headline.replaceWith(new_headline);

    var detail_info = $("#detail_info")[0];
    detail_info.dataset.name = val;
}



function edit_detail_headline(btn){
    var headline = $("#headline_detail")[0];
    var detail_info = $("#detail_info")[0];

    var current_name = detail_info.dataset.name;
    create_input_field(headline, current_name, create_headline); //in pattern_input_field

}

function edit_param_field(param_div, param){

    create_input_field(param_div, param , create_param_field);
}

function create_param_field(val) {
    var param_div = document.createElement("div");
    param_div.setAttribute("onclick", "edit_param_field(this, '"+ escapeHtml(val) +"')");

    var param_content = set_param_field(val);
    param_div.appendChild(param_content);

    return param_div;
}

function set_param_field(param_val){
    var new_text_field = document.createElement("h4");
    new_text_field.appendChild(document.createTextNode(param_val));
    return new_text_field;

}

function go_to_detail_view(elem){
    var detail_info = $("#detail_info")[0];
    var set_specific_info = eval(detail_info.dataset.set_info)

    set_specific_info(elem);
    set_detail_headline(elem.dataset.name);
    enable_detail_headline_btns();

    var create_detail_view = eval(detail_info.dataset.func)

    var detail_view = create_detail_view(elem);
    add_detail_view(detail_view);

    set_buttons(detail_info);
}

function add_detail_view(elem){
    var detail_view = $("#data_detail_list");
    detail_view.html("");
    detail_view[0].appendChild(elem);
}

function save_detail(){
    var detail_info = $("#detail_info")[0];
    var save_detail_specific = eval(detail_info.dataset.save_func);
    save_detail_specific(detail_info);

}

function toggle_services(btn, func_enable, func_disable){
    if(!check_disabled(btn)){
        var detail_info = $("#detail_info")[0];
        if(btn.dataset.status == "0"){
            func_enable(detail_info);
        }else if(btn.dataset.status == "1"){
            func_disable(detail_info);
        }
    }
}


function watch_services(detail_info){
    var watch_services_specific = eval(detail_info.dataset.watch_func)
    watch_services_specific(detail_info);
}

function unwatch_services(detail_info){
    var unwatch_services_specific = eval(detail_info.dataset.unwatch_func)
    unwatch_services_specific(detail_info);
}


function run_services(detail_info){
    var run_services_specific = eval(detail_info.dataset.run_func)
    run_services_specific(detail_info);
}

function stop_services(detail_info){
    var stop_services_specific = eval(detail_info.dataset.stop_func)
    stop_services_specific(detail_info);
}

function set_buttons(detail_info){
   var set_buttons_specific = eval(detail_info.dataset.set_buttons)
   set_buttons_specific(detail_info);
}

function toggle_run_button(btn, btn_status){
    toggle_button(btn, btn_status, "fa-play", "fa-stop");
}

function toggle_watch_button(btn, btn_status){
    toggle_button(btn, btn_status, "fa-eye", "fa-eye-slash");
}