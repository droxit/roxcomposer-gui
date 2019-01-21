function get_services() {
    var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
	$.post("get_services", {
	    csrfmiddlewaretoken: CSRFtoken,
	}).done(function(data) {
	    // Get list mapping service name to its JSON data.
	    tmp = data['local_services'];
	    // Create list to store converted data.
	    name_info_list = [];
	    // Convert JSON data to string.
	    for (var i = 0; i < tmp.length; i++) {
	        var name = tmp[i][0];
	        var json = JSON.stringify(tmp[i][1]);
	        name_info_list.push([name, json]);
	    }
	    // Add service data to list.
	    add_data_entries(name_info_list);
	});
}

function show_empty_detail_view(){
    $("#data_detail_list").html("");
    var detail_headline = $("#headline_detail");

    detail_headline.html("<h4>Select a service.</h4>");


}