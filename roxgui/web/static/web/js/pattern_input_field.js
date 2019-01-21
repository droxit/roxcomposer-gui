function create_input_field(placeholder){
    var input_field = document.createElement("input");
    input_field.setAttribute("type", "text");
    input_field.setAttribute("placeholder", placeholder);
    input_field.setAttribute("class","form-control");

    input_field.addEventListener("keyup", function(e){
        e.preventDefault();
        if(e.keyCode == 13){
            var new_info = input_field.value;
            var new_info_header = document.createElement("h4");
            new_info_header.appendChild(document.createTextNode(new_info));
            input_field.replaceWith(new_info_header);
        }
    });
    return input_field;
}