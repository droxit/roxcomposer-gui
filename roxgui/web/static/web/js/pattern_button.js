/* encoding: utf-8
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
function show_tooltip(btn, success, successmsg, failmsg){
    btn.attr("data-toggle", "popover");
    btn.attr("data-placement", "top");
    btn.attr("data-container", "body");
    var oldTooltip = "";
    if(btn[0].dataset.title){
        oldTooltip = btn[0].dataset.title;
    }

    if(success){
        btn.attr("data-content", successmsg);
    }else{
        btn.attr("data-content", failmsg);
    }
    btn.tooltip("hide");
    btn.popover("show");

    setTimeout(function(){
        btn.popover('dispose');
        btn.attr("data-placement", "bottom");
        if(oldTooltip != ""){
            btn.attr("data-title", oldTooltip);
            btn.attr("data-toggle", "tooltip");
        }
    }, 5000)

}

/* toggles a specific button with two states (e.g. the watch or run buttons) to the other state.
    img1 is the icon for the first state and img2 for the second. These buttons must have a dataset.status info
    that can be either 0 or 1 (for on and off). */
function toggle_button(btn, new_btn_status, img1, img2, tooltip_off, tooltip_on){
    var btn_span = btn.childNodes[1];
    var old_btn_status = btn.dataset.status;
    if(new_btn_status != old_btn_status){
        if(btn.dataset.status == "0"){
            btn.dataset.status = "1"
            btn_span.classList.replace(img1, img2);
            $("#"+btn.id).tooltip('hide').attr('data-original-title', tooltip_on).tooltip('hide');
        }else{
            btn.dataset.status = "0"
            btn_span.classList.replace(img2, img1);
            $("#"+btn.id).tooltip('hide').attr('data-original-title', tooltip_off).tooltip('hide');
        }
    }
}

/* check if the class list of an element contains 'disabled */
function check_disabled(btn){
    return btn.classList.contains("disabled");
}

