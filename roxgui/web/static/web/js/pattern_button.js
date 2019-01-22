function tooltip_run(element, success, successmsg, failmsg){
    var btn = $("#"+element+"");
    btn[0].setAttribute("data-toggle", "tooltip");
    btn[0].setAttribute("data-placement", "bottom");
    if(success){
        btn[0].setAttribute("title", successmsg);
    }else{
        btn[0].setAttribute("title", failmsg);
    }
    btn.tooltip().mouseover();

}