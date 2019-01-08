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

function get_msg_status(elem) {
	var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
	$.post("get_msg_status", {
		csrfmiddlewaretoken: CSRFtoken
	}).done(function(data) {
		for (var msg in data) { //for every message append a card to accordion
			var obj = data[msg];
			//check if card exists
			if (document.getElementById("card-" + obj.message.id) != null) {
				card = document.getElementById("card-" + obj.message.id);
				if (card.dataset.status != "finalized")
					card = update_card(card, obj); // if yes and the msg isn't already finalized, update the status
				//if it's already finalized, don't do anything
			} else {
				create_message_card(elem, obj); // no message card under that id, create a new card for the message
			}
		}

		check_old_cards(data, document.getElementById("accordion")); //delete all the old cards from accordion


	});
}

function check_old_cards(msg_data, accordion) { // call to delete old cards
	var msg_ids = [];
	for (var msg in msg_data) {
		msg_ids.push(msg)
	}
	var cards = accordion.children;

	for (var i in cards) {
		if (cards[i].nodeType == 1) {
			var card = cards[i];
			var card_id = card.id.substring(5, card.id.length);
			if (!msg_ids.includes(card_id))
				card.remove()
		}
	}

}

function update_card(card, obj) {
	if (obj.status != null) {
		if (obj.status.status != card.dataset.status) { // if status changed update the status
			update_status(card, obj);
		} else {
			update_processing();
		}
	} else {
		update_no_info(card, obj);
	}
}

function update_processing(card, obj) { // call only if the status has changed to processing
	//update current service
	var div_cardbody = card.querySelector("#card-body-" + obj.message.id);
	span_cur_serv = div_cardbody.querySelector("#CurrentService-" + obj.message.id);
	make_status_text(span_cur_serv, "Current Service", obj.status.service_name);

	//update processing time
	if (obj.status.processing_time != null) {

		span_processing_time = div_cardbody.querySelector("#ProcessingTime-" + obj.message.id);
		make_status_text(span_processing_time, "Processing Time", obj.status.processing_time);
	}

}

function update_finalized(card, obj) { // call if the status has changed to finalized
	if (obj.status.status == "finalized") {
		var heading = card.querySelector("#heading-" + obj.message.id);
		heading.className = "card-header bg-success text-white";
		card.setAttribute("data-status", "finalized");

		//update Finished text
		var div_cardbody = card.querySelector("#card-body-" + obj.message.id);
		span_finished = div_cardbody.querySelector("#Finished-" + obj.message.id);
		make_status_text(span_finished, "Finished at", obj.status.time);

		//update total processing time
		if (obj.status.total_processing_time != null) {
			span_finished = div_cardbody.querySelector("#TotalProcessingTime-" + obj.message.id);
			make_status_text(span_finished, "Total Processing Time", obj.status.total_processing_time, obj.message.id);
		}

		//delete processing time, current service
		span_cur_serv = div_cardbody.querySelector("#CurrentService-" + obj.message.id);
		span_cur_serv.innerHTML = "";

		span_processing_time = div_cardbody.querySelector("#ProcessingTime-" + obj.message.id);
		span_processing_time.innerHTML = "";

	}

}

function update_error(card, obj) {
	//we don't know yet what happens when an error occurs
}

function update_no_info(card, obj) { // call if there is no status information for a message
	var heading = card.querySelector("#heading-" + obj.message.id);
	heading.className = "card-header";

	var div_cardbody = card.querySelector("#card-body-" + obj.message.id);
	div_cardbody.appendChild(document.createTextNode("No further information available"));
}

function update_status(card, obj) { // call only if the whole status of the message has changed

	//update the status in card header (color), card header span and span inside card body
	var heading = card.querySelector("#heading-" + obj.message.id);
	heading.setAttribute("data-status", obj.status.status);

	//update status in the card header
	var span = card.querySelector("#status-" + obj.message.id);
	span.innerHTML = "";
	span.appendChild(document.createTextNode(obj.status.status));

	//update status inside the info card
	var div_cardbody = card.querySelector("#card-body-" + obj.message.id);
	span_status = div_cardbody.querySelector("#Status-" + obj.message.id);
	make_status_text(span_status, "Status", obj.status.status);

	if (obj.status.status == "processing") { // if the status is now processing, change the status info in card body accordingly
		heading.className = "card-header bg-warning text-white"; // color of the header depends on status
		update_processing(card, obj);
	} else if (obj.status.status == "error") {
		heading.className = "card-header bg-danger text-white";
		update_error(card, obj);
	} else if (obj.status.status == "finalized") {
		heading.className = "card-header bg-success text-white";
		update_finalized(card, obj);
	}

}


function create_message_card(elem, obj) { //create the whole message card element corresponding to the message in obj
	id = obj.message.id;

	var carddiv = document.createElement("div");
	carddiv.className = "card";
	carddiv.setAttribute("id", "card-" + id);
	carddiv.setAttribute("data-status", null);
	elem.appendChild(carddiv);

	//<<<<<<<<<<<HEADER>>>>>>>>>>>>>
	var cardheader = document.createElement("div");
	cardheader.setAttribute("id", "heading-" + id);
	cardheader.setAttribute("data-toggle", "collapse");
	cardheader.setAttribute("data-target", "#m" + id);
	cardheader.setAttribute("data-status", null);
	cardheader.setAttribute("aria-expanded", "false");
	cardheader.setAttribute("aria-controls", "m" + id);
	cardheader.className = "card-header";

	carddiv.appendChild(cardheader);

	var div_flex = document.createElement("div");
	div_flex.setAttribute("class", "d-flex");
	cardheader.appendChild(div_flex);

	var div_col = document.createElement("div");
	div_col.setAttribute("class", "col-mb-9");
	div_col.appendChild(document.createTextNode(obj.message.message))
	div_flex.appendChild(div_col);

	var div_col1 = document.createElement("div");
	div_col1.setAttribute("class", "ml-auto");

	var span = document.createElement("span");
	span.setAttribute("id", "status-" + id)
	span.setAttribute("style", "font-size:0.7em");
	span.setAttribute("data-status", null);
	div_col1.appendChild(span);
	div_flex.appendChild(div_col1);
	//<<<<<<<<<<<HEADER END>>>>>>>>>>>>>>>>

	//<<<<<<<<<<<STATUS DIV>>>>>>>>>>>>>>>>
	var div2 = document.createElement("div");
	div2.setAttribute("id", "m" + id);
	div2.setAttribute("aria-labelledby", "heading-" + id);
	div2.setAttribute("data-parent", "#accordion")
	div2.setAttribute("class", "collapse")
	carddiv.appendChild(div2);

	var div_cardbody = document.createElement("div");
	div_cardbody.setAttribute("class", "card-body");
	div_cardbody.setAttribute("id", "card-body-" + id);
	div2.appendChild(div_cardbody);

	//Text
	var text_arr = ["ID", "Pipeline", "Status", "CurrentService", "ProcessingTime", "Started", "Finished", "TotalProcessingTime"];

	for (var i in text_arr) {
		let span_text = text_arr[i];
		var spn = document.createElement("span");
		spn.setAttribute("id", span_text + "-" + id);
		div_cardbody.appendChild(spn);
	}

	span_id = div_cardbody.querySelector("#ID-" + id);
	make_status_text(span_id, "ID", id);

	span_pipe = div_cardbody.querySelector("#Pipeline-" + id);
	make_status_text(span_pipe, "Pipeline", obj.message.pipeline);

	span_started = div_cardbody.querySelector("#Started-" + id);
	make_status_text(span_started, "Started at", obj.message.time);

	update_status(carddiv, obj);

	return elem;
}


function make_status_text(node, text, obj) {
	node.innerHTML = "";
	var sm = document.createElement("small");
	var br = document.createElement("br");
	node.appendChild(document.createTextNode(text + ": "));
	node.appendChild(sm);
	sm.appendChild(document.createTextNode(obj));
	node.appendChild(br);
}
