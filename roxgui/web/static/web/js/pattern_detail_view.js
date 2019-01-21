function create_headline(name){
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
}

function set_info(elem_name){
    $("#detail_info")[0].dataset.name = elem_name;
}

function edit_detail_headline(){
    var headline = $("#headline_detail");
    var detail_info = $("#detail_info")[0];

    var current_name = detail_info.dataset.name;
    var new_info_container = document.createElement("h4");
    create_input_field(headline, current_name, create_headline); //in pattern_input_field
}

function enable_detail_headline_btns(){
    ["btn-edit","btn-delete","btn-watch"].forEach(function(btn){
        btn_remove_disabled(btn);
    });
}

function btn_remove_disabled(btn){
    var btnedit = $("#"+btn+"")[0];
    btnedit.classList.remove("disabled");
}

function go_to_detail_view(elem){
    set_info(elem.dataset.name);
    set_detail_headline(elem.dataset.name);
    enable_detail_headline_btns();
}