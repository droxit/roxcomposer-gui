/*
#
# Define web views.
#
# devs@droxit.de
#
# Copyright (c) 2018 droxIT GmbH
#
*/

/* Retrieve the current logs from the server and create the corresponding text inside the log window. */
function update_log(log_win) {
	var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
	$.post("get_watch_logs", {
		csrfmiddlewaretoken: CSRFtoken
	}).done(function(data) {
		for (var log in data) { //for every log append a log line to log window
			var obj = data[log];
			//check if log line is new, then update the log
			if (document.getElementById("log-" + obj.id) == null) {
				create_logline(log_win, obj);
			}
		}

		check_old_logs(data, log_win); //delete all the old loglines
	});
}

/* Append the text node in the log window for one log line. */
function create_logline(log_win, log) {
	id = log.id;

	var span = document.createElement("span");
	span.setAttribute("id", "log-" + id);
	//span.setAttribute("style", "font-size:0.7em");
	make_logline_text(span, log);
	log_win.appendChild(span);
}

/* Create the text node for one log line. */
function make_logline_text(node, logline) {
	var br = document.createElement("br");
	node.appendChild(document.createTextNode(logline.text));
	node.appendChild(br);
}

/* Check if the log window contains logs that were not sent by the server,
    meaning they expired and should be removed. */
function check_old_logs(log_win, log_data) {
	var log_ids = [];
	for (var log in log_data) {
		log_ids.push(log)
	}
	var logs = log_win.children;

	for (var i in logs) {
		if (logs[i].nodeType == 1) {
			var logline = logs[i];
			var log_id = logline.id.substring(4, logline.id.length);
			if (!log_ids.includes(log_id))
				logline.remove();
		}
	}
}


/* Reloads the log information every few seconds and updates the log window. */
function reload_logs(){
    // Update constantly reloaded elements.
    log_win = document.getElementById("log");
    setInterval(function() {
        update_log(log_win);
    }, 1000);
}