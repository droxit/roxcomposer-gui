/*
# encoding: utf-8
#
# Define web views.
#
# devs@droxit.de
#
# Copyright (c) 2018 droxIT GmbH
#
*/

function add_optional_param() {
    // Get parent element.
    var parent = document.getElementById("service_optional_fields");
    // Create key input field.
    var key_div = document.createElement("div");
    key_div.setAttribute("class", "col-sm-4");
    var key_input = document.createElement("input");
    key_input.setAttribute("type", "text");
    key_input.setAttribute("class", "form-control");
    key_input.setAttribute("id", "key");
    key_input.setAttribute("placeholder", "Key");
    key_div.appendChild(key_input);
    // Create value input field.
    var value_div = document.createElement("div");
    value_div.setAttribute("class", "col-sm-8");
    var value_input = document.createElement("input");
    value_input.setAttribute("type", "text");
    value_input.setAttribute("class", "form-control");
    value_input.setAttribute("id", "value");
    value_input.setAttribute("placeholder", "Value");
    value_div.appendChild(value_input);
    // Append both inputs to form group.
    var form_group_div = document.createElement("div");
    form_group_div.setAttribute("class", "form-group row");
    form_group_div.appendChild(key_div);
    form_group_div.appendChild(value_div);
    // Append all elements to corresponding parent tag.
    parent.appendChild(form_group_div);
}

function remove_optional_param() {
    var parent = document.getElementById("service_optional_fields");
    parent.removeChild(parent.lastChild);
}

function create_result_message(data) {
    var result_msg = document.createElement("div");
    if (data.success) {
        if (data.message) {
            // Request successful but with warnings.
            result_msg.setAttribute("class", "alert alert-warning");
            result_msg.innerHTML = data.message;
        } else {
            // Request successful without any warnings.
            result_msg.setAttribute("class", "alert alert-success");
            result_msg.innerHTML = "Success.";
        }
    } else {
        if (data.message) {
            // Request failed with error message.
            result_msg.setAttribute("class", "alert alert-danger");
            result_msg.innerHTML = data.message;
        } else {
            // Request failed without error message.
            result_msg.setAttribute("class", "alert alert-danger");
            result_msg.innerHTML = "Failure.";
        }
    }
    return result_msg;
}

function send_params() {
    // Get mandatory parameters.
    var ip = document.getElementById("ip").value;
    var port = document.getElementById("port").value;
    var name = document.getElementById("name").value;
    var class_path = document.getElementById("class_path").value;
    // Get optional parameters.
    var optional = document.getElementById("service_optional_fields");
    // Extract key and corresponding value of each optional parameter.
    var optional_param_keys = [];
    var optional_param_values = [];
    var child;
    var key;
    var value;
    for (i = 0; i < optional.childNodes.length; i++) {
        child = optional.childNodes[i];
        key = child.querySelector("#key").value;
        value = child.querySelector("#value").value;
        optional_param_keys.push(key);
        optional_param_values.push(value);
    }
    // Create CSRF token.
    var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
    // Create service parameter dictionary.
    params = {
        ip: ip,
        port: port,
        name: name,
        class_path: class_path,
        optional_param_keys: optional_param_keys,
        optional_param_values: optional_param_values,
        csrfmiddlewaretoken: CSRFtoken
    };
    // Create service with specified parameters.
    $.post("create_service", params).done(function(data) {
        // Get element which should contain result messages.
        var msg_div = document.getElementById("service_params_message");
        // Create result message.
        var result_msg = create_result_message(data);
        // Add result message to corresponding parent element.
        msg_div.appendChild(result_msg);
        // Remove error message after a few seconds.
        setTimeout(
            function() {
                result_msg.remove();
            },
            5000
        );
    });
}