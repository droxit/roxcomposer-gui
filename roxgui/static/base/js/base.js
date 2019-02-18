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
	$.post("check_rox_settings", {
		csrfmiddlewaretoken: CSRFtoken
	}).done(function(data) {

		var text = "";
		var port_input = false;
		var path_input = false;
		var open_modal_flag = false;

		if(!data.running){
		    text += "Attention! The ROXcomposer is not running. Please start the ROXcomposer. \n";
		    open_modal_flag = true;
		}
		if(!data.path_set){
		    text += "The path to the ROXcomposer is not set correctly, please provide a valid path below. \n";
		    path_input = true;
		    open_modal_flag = true;
		}
		if(!data.port_set){
		    text += "The port on which the ROXcomposer can be found is not set, please provide a valid port. \n";
		    port_input = true;
		    open_modal_flag = true;
		}

        if(open_modal_flag){
		    open_modal(text, path_input, port_input);
        }

	});
}

/* Opens a Modal that shows the specified text and input fields. */
function open_modal(text, path_flag, port_flag){

   var inputs = ""
   if(path_flag){
       inputs += "<div> \
                    <p> ROXcomposer path: </p> \
                    <input id='rox_path' placeholder='Path to your ROXcomposer installation..'></input> \
                 </div>";
   }
   if(port_flag){
       inputs += "<div> \
                    <p> Port: </p> \
                    <input id='rox_port' placeholder='Port on which the ROXcomposer is running...'></input> \
                 </div>";
   }

   var modal_warning = $("<div class='modal' tabindex='-1' role='dialog'> \
  <div class='modal-dialog' role='document'> \
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
          <div> \
            "+ inputs +" \
          </div> \
      </div> \
      <div class='modal-footer'> \
        <button type='button' class='btn btn-primary' onclick='set_rox_settings(this, "+path_flag+","+port_flag+")'>Delete</button> \
        <button type='button' class='btn btn-secondary' data-dismiss='modal'>Close</button> \
      </div> \
    </div> \
  </div> \
</div>");

	popup_warning.modal("toggle");

}



function set_rox_settings(btn, path_flag, port_flag){
    var specified_port = "";
    var specified_path = "";

    if(path_flag){
        var path_input = document.getElementById("path_input");
        var specified_path = path_input.value();
    }

    if(port_flag){
        var port_input = document.getElementById("port_input");
        var specified_port = port_input.value();
    }

    var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
	$.post("set_rox_settings", {
		csrfmiddlewaretoken: CSRFtoken,
		port: specified_port,
		path: specified_path
	}).done(function(data) {

		if(!data.success){
		    // show red tooltip with error message
		}

	});
}