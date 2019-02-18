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
    enter a Path to the ROXcomposer's installation folder and the port on which the ROXcomposer is running.*/
function check_rox_running(){
    var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
	$.post("check_rox", {
		csrfmiddlewaretoken: CSRFtoken
	}).done(function(data) {

		// do things

	});
}