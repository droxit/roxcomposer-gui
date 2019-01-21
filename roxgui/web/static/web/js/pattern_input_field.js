function create_input_field(text_node, placeholder, new_info_container){
    //text_node is the place where the input field should reside (the text that gets replaced)
    //placeholder is the text that was in the textnode first
    //new_info_container is an html element with the correct format for the new output
    var input_field = document.createElement("input");
    input_field.setAttribute("type", "text");
    input_field.setAttribute("placeholder", placeholder);
    input_field.setAttribute("class","form-control");

    input_field.addEventListener("keyup", function(e){
        e.preventDefault();
        if(e.keyCode == 13){
            var new_info = input_field.value;
            new_info_container.appendChild(document.createTextNode(new_info));
            input_field.replaceWith(new_info_container);
        }
    });

    text_node.replaceWith(input_field);
}