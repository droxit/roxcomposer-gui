/*
#
# Define the pattern for popovers and togglable buttons.
#
# devs@droxit.de
#
# Copyright (c) 2019 droxIT GmbH
#
*/


/* Shows a popover message on the element 'btn' depending on the boolean 'success'.
   If true 'successmsg' will be shown, else the 'failmsg' string.
   If there is a tooltip on the element it will be removed for the duration of the popover,
   but will be reinitialised after. */
function show_tooltip(btn, success, successmsg, failmsg) {
    // delete old tooltip and save the content
    var oldTooltip = "";
	if (btn[0].dataset.title) {
		oldTooltip = btn[0].dataset.title;
		btn[0].dataset.title = "";
	}
	btn.tooltip('dispose');
    btn.popover('dispose');

    // create popover
    var jbtn = $(btn);
    btn.popover({placement:'bottom', title:''});
    var popover = btn.data('bs.popover');
    popover.tip()

    // depending on success set the color and content of popover
	if (success) {
	    popover.config.title = "";
		popover.config.content = successmsg;
        btn.popover('show');
        btn.data('bs.popover').tip.classList.add('popover-success');
	} else {
        popover.config.content = failmsg;
        btn.popover('show');
        btn.data('bs.popover').tip.classList.add('popover-danger');
	}

    // delete popover and put tooltip back in place
	setTimeout(function() {
		btn.popover('dispose');
		btn.tooltip({title: oldTooltip, placement:'bottom'})
	}, 5000)
}

/* Remove the popover from this element */
function remove_tooltip(elem){
    elem.popover('dispose')
}



function add_tooltip(btn_id, tooltip_string){
    console.log($("#"+btn_id))
    $("#"+btn_id).tooltip({
        placement: "bottom",
        toggle: "tooltip",
        title: tooltip_string
    });
}

/* toggles a specific button with two states (e.g. the watch or run buttons) to the other state.
    img1 is the icon for the first state and img2 for the second. These buttons must have a dataset.status info
    that can be either 0 or 1 (for on and off). */
function toggle_button(btn, new_btn_status, img1, img2, tooltip_off, tooltip_on) {
	var btn_span = btn.childNodes[0];
	var old_btn_status = btn.dataset.status;
	if (new_btn_status != old_btn_status) {
		if (btn.dataset.status == "0") {
			btn.dataset.status = "1"
			btn_span.classList.replace(img1, img2);
			$(btn).tooltip('hide');
			$(btn).tooltip({title: tooltip_on});
			$(btn).tooltip('hide');
		} else {
			btn.dataset.status = "0"
			btn_span.classList.replace(img2, img1);
			$(btn).tooltip('hide');
			$(btn).tooltip({title: tooltip_off});
			$(btn).tooltip('hide');
		}
	}
}

/* check if the class list of an element contains 'disabled */
function check_disabled(btn) {
	return btn.classList.contains("disabled");
}
