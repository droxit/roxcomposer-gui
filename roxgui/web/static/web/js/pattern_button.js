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


function toggle_button(btn, detail_info, success, img1, img2){
    var btn_span = btn.childNodes[1];
    if(success){
        if(btn.dataset.status == "0"){
                btn.dataset.status = "1"
                btn_span.classList.replace(img1, img2);
        }else{
            btn.dataset.status = "0"
            btn_span.classList.replace(img2, img1);
        }
    }
}

function check_disabled(btn){
    return btn.classList.contains("disabled");
}