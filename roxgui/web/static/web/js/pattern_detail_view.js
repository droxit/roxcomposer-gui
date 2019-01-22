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

function set_info(elem_name, elem_title){
    $("#detail_info")[0].dataset.name = elem_name;
    $("#detail_info")[0].dataset.title = elem_title;
}

function edit_detail_headline(btn){
    if(!check_disabled(btn)){
        var headline = $("#headline_detail")[0];
        var detail_info = $("#detail_info")[0];

        var current_name = detail_info.dataset.name;
        create_input_field(headline, current_name, create_headline); //in pattern_input_field
    }
}

function enable_detail_headline_btns(){
    //"btn-watch" ,"btn-delete", "btn-save"
    ["btn-edit", "btn-run"].forEach(function(btn){
        btn_remove_disabled(btn);
    });
}

function btn_remove_disabled(btn){
    var btnedit = $("#"+btn+"")[0];
    btnedit.classList.remove("disabled");
}

function go_to_detail_view(elem){
    set_info(elem.dataset.name, elem.dataset.title);
    set_detail_headline(elem.dataset.name);
    enable_detail_headline_btns();

    var detail_info = $("#detail_info")[0];
    var create_detail_view = eval(detail_info.dataset.func)

    var detail_view = create_detail_view(elem);
    add_detail_view(detail_view);
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

function toggle_services(btn){
    if(!check_disabled(btn)){
        var detail_info = $("#detail_info")[0];
        if(btn.dataset.status == "0"){
            run_services(detail_info);
        }else if(btn.dataset.status == "1"){
            stop_services(detail_info);
        }
    }
}

function run_services(detail_info){
    var run_services_specific = eval(detail_info.dataset.run_func)
    run_services_specific(detail_info);
}



function stop_services(detail_info){
    var stop_services_specific = eval(detail_info.dataset.stop_func)
    stop_services_specific(detail_info);
}