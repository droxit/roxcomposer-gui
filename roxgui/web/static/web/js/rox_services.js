function show_empty_detail_view(){
    $("#data_detail_list").html("");
    var detail_headline = $("#headline_detail");

    detail_headline.html("<h4>Select a service.</h4>");


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

function get_params(service){
    var json_params = JSON.parse(service.title);
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

function run_service(detail_info){
    var service = detail_info.dataset.name;
    var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
	$.post("start_services", {
		services: [service],
		csrfmiddlewaretoken: CSRFtoken
	}).done(function(data) {
		// TODO: if error show tooltip
		console.log(data)
		if(data.success){
		    update_run_button();
		}
		show_tooltip(element, data.success, "Started service successfully.", "Failed to start service");
	});
}

function update_run_button(){

}