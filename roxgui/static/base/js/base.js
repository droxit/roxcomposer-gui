/*
# JS functions that are needed for the whole site.
#
# devs@droxit.de
#
# Copyright (c) 2019 droxIT GmbH
#
*/

$('[data-toggle="tooltip"]').tooltip({ // Enable bootstrap tooltips
	container: 'body'
});


/* This function is called on every website to check if the roxcomposer is running.
    If it is not running it will open a modal on the current website that prompts the user to
    enter a Path to the ROXcomposer's installation folder and the port on which the ROXcomposer is running.
    The response from the server should contain:
     - port_set : boolean | true if the port to the roxcomposer is set in the config file
     - path_set : boolean | true if the path to the roxcomposer is set in the config file
     - running : boolean | true if the roxcomposer was identified as running on the specified port
*/
function check_rox_running() {
	$.get("check_rox_settings", {}).done(function(res) {
		var text = "";
		var port_input = false;
		var path_input = false;
		var ip_input = false;
		var open_modal_flag = false;

        var current_ip = ""
		var current_port = "";
		var current_path = "";


		if (!res.data.running) {
			text += "<div><p><h4><b>Attention!</b></h4> The ROXcomposer is <b>not running</b>. Please start the ROXcomposer. </p></div>";
			open_modal_flag = true;
		}
		if (!res.data.ip_set) {
			text += "<div><p>The <b>IP</b> is not set, please provide a valid IP.</p></div>";
			ip_input = true;
			open_modal_flag = true;
			current_ip = res.data.ip;
		}
		if (!res.data.port_set) {
			text += "<div><p>The <b>port</b> on which the ROXcomposer can be found is not set, please provide a valid port.</p></div>";
			port_input = true;
			open_modal_flag = true;
			current_port = res.data.port
		}
		if (!res.data.path_set) {
			text += "<div><p>The <b>path</b> to the ROXcomposer is not set correctly, please provide a valid path below.</p></div>";
			path_input = true;
			open_modal_flag = true;
			current_path = res.data.path;
		}

		if (!res.success) {
			open_modal(text, path_input, port_input, ip_input, current_path, current_port, current_ip);
		}

	});
}

/* Opens a Modal that shows the specified text and input fields. */
function open_modal(text, path_flag, port_flag, ip_flag, current_path, current_port, current_ip) {

	var inputs = ""
	if (path_flag) {
		inputs += "<div class='col-md-4'> \
                    <p> Path: </p> \
                  </div> \
                  <div class='col-md-8'> \
                    <input class='form-control' value="+current_path+" type='text' id='rox_path' placeholder='Path to ROXcomposer installation..'></input> \
                 </div>";
	}
	if (port_flag) {
		inputs += "<div class='col-md-4'> \
                    <p> Port: </p> \
                  </div> \
                  <div class='col-md-8'> \
                    <input class='form-control' value="+current_port+" type='number' id='rox_port' placeholder='Port of ROXcomposer..'></input> \
                 </div>";
	}
	if (ip_flag) {
		inputs += "<div class='col-md-4'> \
                    <p> IP: </p> \
                  </div> \
                  <div class='col-md-8'> \
                    <input class='form-control' value="+current_ip+" type='text' id='rox_ip' placeholder='IP of ROXcomposer..'></input> \
                 </div>";
	}

	var modal_warning = $("<div class='modal' tabindex='-1' role='dialog' id='settings_modal'> \
  <div class='modal-dialog' role='document' style='min-width:800px'> \
    <div class='modal-content'> \
      <div class='modal-header'> \
        <h5 class='modal-title'> ROXcomposer settings</h5> \
        <button type='button' class='close' data-dismiss='modal' aria-label='Close'> \
          <span aria-hidden='true'>&times;</span> \
        </button> \
      </div> \
      <div class='modal-body'> \
          <div> \
            <p>" + text + "</p> \
          </div> \
          <div class='row'> \
            " + inputs + " \
          </div> \
      </div> \
      <div class='modal-footer'> \
        <button type='button' id='settings_btn' class='btn btn-primary' onclick='set_rox_settings(" + path_flag + "," + port_flag + "," + ip_flag + ")'>Set</button> \
        <button type='button' class='btn btn-secondary' data-dismiss='modal'>Close</button> \
      </div> \
    </div> \
  </div> \
</div>");
	modal_warning.modal("toggle");

}


/* Set the rox settings in the modal with the specified values in the inputs.
    Depending on which flags (path, port, ip) are set to true these values are checked and
    submitted to the server. */
function set_rox_settings(path_flag, port_flag, ip_flag){
    var specified_port = null;
    var specified_path = null;
    var specified_ip = null;

    var show_empty_error = false;

	if (ip_flag) {
		var ip_input = document.getElementById("rox_ip");
		specified_ip = ip_input.value;
		if(specified_ip == ""){
		    show_empty_error = true;
		}
	}
	if (port_flag) {
		var port_input = document.getElementById("rox_port");
		specified_port = port_input.value;
		if(specified_port == ""){
		    show_empty_error = true;
		}
	}
	if (path_flag) {
		var path_input = document.getElementById("rox_path");
		specified_path = path_input.value;
		if(specified_path == ""){
		    show_empty_error = true;
		}
	}

	var btn = $("#settings_btn");
    btn.popover();
    var popover = btn.data('bs.popover');
    popover.config.placement = "bottom";
    // popover.config.content = data.message;
    //btn.popover('show');

	if(show_empty_error){
	    popover.config.content = "Input in all fields is required.";
        btn.popover('show');
        btn.data('bs.popover').tip.classList.add('popover-danger');
	} else{

        var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
        $.post("update_rox_settings", {
            csrfmiddlewaretoken: CSRFtoken,
            ip: specified_ip,
            port: specified_port,
            path: specified_path
        }).done(function(data) {

            if(!data.success){
                // show red tooltip with error message
                popover.config.content = data.message;
                btn.popover('show');
                btn.data('bs.popover').tip.classList.add('popover-danger');
            } else {
                $('#settings_modal').modal('hide');
            }
        });
    }
}
