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
function check_rox_running(){

    var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
	$.post("check", {
		csrfmiddlewaretoken: CSRFtoken
	}).done(function(res) {
		var text = "";
		var port_input = false;
		var path_input = false;
		var ip_input = false;
		var open_modal_flag = false;

		if(!res.data.running){
		    text += "<div><p><h4><b>Attention!</b></h4> The ROXcomposer is <b>not running</b>. Please start the ROXcomposer. </p></div>";
		    open_modal_flag = true;
		}
		if(!res.data.path){
		    text += "<div><p>The <b>path</b> to the ROXcomposer is not set correctly, please provide a valid path below.</p></div>";
		    path_input = true;
		    open_modal_flag = true;
		}
		if(!res.data.port){
		    text += "<div><p>The <b>port</b> on which the ROXcomposer can be found is not set, please provide a valid port.</p></div>";
		    port_input = true;
		    open_modal_flag = true;
		}
		if(!res.data.ip){
		    text += "<div><p>The <b>IP</b> is not set, please provide a valid IP.</p></div>";
		    ip_input = true;
		    open_modal_flag = true;
		}

        if(!res.success){
		    open_modal(text, path_input, port_input, ip_input);
        }

	});
}

/* Opens a Modal that shows the specified text and input fields. */
function open_modal(text, path_flag, port_flag, ip_flag){

   var inputs = ""
   if(path_flag){
       inputs += "<div class='col-md-4'> \
                    <p> Path: </p> \
                  </div> \
                  <div class='col-md-8'> \
                    <input class='form-control' type='text' id='rox_path' placeholder='Path to ROXcomposer installation..'></input> \
                 </div>";
   }
   if(port_flag){
       inputs += "<div class='col-md-4'> \
                    <p> Port: </p> \
                  </div> \
                  <div class='col-md-8'> \
                    <input class='form-control' type='number' id='rox_port' placeholder='Port of ROXcomposer..'></input> \
                 </div>";
   }
   if(ip_flag){
       inputs += "<div class='col-md-4'> \
                    <p> IP: </p> \
                  </div> \
                  <div class='col-md-8'> \
                    <input class='form-control' type='text' id='rox_ip' placeholder='IP of ROXcomposer..'></input> \
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
            <p>"+ text +"</p> \
          </div> \
          <div class='row'> \
            "+ inputs +" \
          </div> \
      </div> \
      <div class='modal-footer'> \
        <button type='button' id='settings_btn' class='btn btn-primary' onclick='set_rox_settings("+path_flag+","+port_flag+","+ip_flag+")'>Set</button> \
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
    var specified_port = "";
    var specified_path = "";
    var specified_ip = "";

    if(path_flag){
        var path_input = document.getElementById("rox_path");
        specified_path = path_input.value;
    }

    if(port_flag){
        var port_input = document.getElementById("rox_port");
        specified_port = port_input.value;
    }
    if(ip_flag){
        var ip_input = document.getElementById("rox_ip");
        specified_ip = ip_input.value;
    }

    var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
	$.post("set_rox_settings", {
		csrfmiddlewaretoken: CSRFtoken,
		port: specified_port,
		path: specified_path,
		ip: specified_ip
	}).done(function(data) {

		if(!data.success){
		    // show red tooltip with error message
		    var btn = $("#settings_btn");
            btn.popover();
            var popover = btn.data('bs.popover');
            popover.config.content = data.message;
            popover.config.placement = "bottom";
            btn.popover('show');
            btn.data('bs.popover').tip.classList.add('popover-danger');
		} else {
		    $('#settings_modal').modal('hide');
		}

	});
}