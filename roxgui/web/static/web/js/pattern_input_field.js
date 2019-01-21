function create_input_field(text_node, placeholder, change_text_node){
    //text_node is the place where the input field should reside (the text that gets replaced)
    //placeholder is the text that was in the textnode first
    //new_info_container is an html element with the correct format for the new output

    var input_field = document.createElement("input");
    input_field.setAttribute("type", "text");
    input_field.setAttribute("placeholder", placeholder);
    input_field.setAttribute("class","form-control");
    input_field.setAttribute("id", text_node.id);

    input_field.addEventListener("keyup", function(e){
        e.preventDefault();
        if(e.keyCode == 13){
            input_save(input_field, placeholder, change_text_node);
        }
    });

    input_field.addEventListener("focusout", function(e){
        e.preventDefault();
        input_save(input_field, placeholder, change_text_node);
    });



    text_node.replaceWith(input_field);
}

function input_save(input_field, placeholder, change_text_node){
    var new_info = input_field.value;
    if(!new_info){
        new_info = placeholder;
    }
    var new_text_node = change_text_node(new_info);
    input_field.replaceWith(new_text_node);
}