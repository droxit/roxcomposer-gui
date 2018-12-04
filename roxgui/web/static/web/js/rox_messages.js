acc = document.getElementById("accordion");
setInterval(function() {

   //acc.innerHTML = "";
   get_msg_status(acc);
}, 1000);


function get_msg_status(elem){
    var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
    $.post("msg_status", {csrfmiddlewaretoken : CSRFtoken}).done(function(data){

        var count = 0;
        for(var msg in data) { //for every message append a card to accordion


            var obj = data[msg];
            console.log(obj["message"]);
            console.log(obj);

            if(document.getElementById("card-" + obj["message"]["id"]) != null){
                card = document.getElementById("card-" + obj["message"]["id"]);
                //update
                card = update_status(card, obj);

            }else{ //create
                 create_message_card(elem, obj);
            }


        }

    });
}

function update_status(card, obj){
    elem = card.querySelector("#heading-"+obj["message"]["id"]);
    if(obj["status"]["status"] != elem.dataset.status){
        if(obj["status"]["status"] == "processing"){
            elem.className = "card-header bg-warning text-white";
        } else if(obj["status"]["status"] == "finalized"){
            elem.className = "card-header bg-success text-white";
        } else if(obj["status"]["status"] == "error"){
            elem.className = "card-header bg-danger text-white";
        } else{
            elem.className = "card-header";
        }
        elem.setAttribute("data-status", obj["status"]["status"])
    }
}

function create_message_card(elem, obj){
    var carddiv = document.createElement("div");
    carddiv.className = "card";
    carddiv.setAttribute("id", "card-"+obj["message"]["id"])
    elem.appendChild(carddiv);

    //<<<<<<<<<<<HEADER>>>>>>>>>>>>>
    var cardheader = document.createElement("div");
    cardheader.setAttribute("id", "heading-" + obj["message"]["id"]);
    cardheader.setAttribute("data-toggle", "collapse");
    cardheader.setAttribute("data-target", "#m" + obj["message"]["id"]);
       cardheader.setAttribute("data-status", "");
    cardheader.setAttribute("aria-expanded", "false");
    cardheader.setAttribute("aria-controls", "m" + obj["message"]["id"]);

    carddiv.appendChild(cardheader);

    update_status(carddiv, obj);

    var div_flex = document.createElement("div");
    div_flex.setAttribute("class", "d-flex");
    //div_flex.setAttribute("")
    cardheader.appendChild(div_flex);

    var div_col = document.createElement("div");
    div_col.setAttribute("class", "col-mb-9");
    div_col.appendChild(document.createTextNode(obj["message"]["message"]))
    div_flex.appendChild(div_col);

    var div_col1 = document.createElement("div");
    div_col1.setAttribute("class", "ml-auto");
    if(obj["status"] != "None" && obj["status"]["status"] != "None"){
        var span = document.createElement("span");
        span.setAttribute("style", "font-size:0.7em");
        span.appendChild(document.createTextNode(obj["status"]["status"]));
        div_col1.appendChild(span);
    }
    div_flex.appendChild(div_col1);
    //<<<<<<<<<<<HEADER END>>>>>>>>>>>>>>>>

    //<<<<<<<<<<<STATUS DIV>>>>>>>>>>>>>>>>

    var div2 = document.createElement("div");
    div2.setAttribute("id", "m" + obj["message"]["id"]);
    div2.setAttribute("aria-labelledby", "heading-"+obj["message"]["id"]);
    div2.setAttribute("data-parent", "#accordion")
    div2.setAttribute("class", "collapse")
    carddiv.appendChild(div2);

    var div_cardbody = document.createElement("div");
    div_cardbody.setAttribute("class", "card-body");
    div2.appendChild(div_cardbody);

    //Text
    div_cardbody = make_status_text(div_cardbody, "ID", obj["message"]["id"]);

    div_cardbody = make_status_text(div_cardbody, "Pipeline", obj["message"]["pipeline"]);

    if(obj["status"] != null){
        div_cardbody = make_status_text(div_cardbody, "Status", obj["status"]["status"]);

        if(obj["status"]["status"] != "finalized"){
            div_cardbody = make_status_text(div_cardbody, "Current Service", obj["status"]["service_name"]);
        }
        if(obj["status"]["processing_time"] != null){
            div_cardbody = make_status_text(div_cardbody, "Processing Time", obj["status"]["processing time"]);
        }
        div_cardbody = make_status_text(div_cardbody, "Started at", obj["message"]["time"]);

        if(obj["status"]["status"] == "finalized"){
            div_cardbody = make_status_text(div_cardbody, "Finished at", obj["status"]["time"]);

            if(obj["status"]["total_processing_time"] != null){
                div_cardbody = make_status_text(div_cardbody, "Total Processing Time", obj["status"]["total_processing_time"]);
            }
        }

    }else{
        div_cardbody.appendChild(document.createTextNode("No further information available"));
    }
    return elem;
}


function make_status_text(node, text, obj){
    var sm = document.createElement("small");
    var br = document.createElement("br");
    node.appendChild(document.createTextNode(text+ ": "));
    node.appendChild(sm);
    sm.appendChild(document.createTextNode(obj));
    node.appendChild(br);
    return node
}