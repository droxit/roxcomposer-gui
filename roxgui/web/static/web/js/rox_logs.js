/*
#
# Define web views.
#
# |------------------- OPEN SOURCE LICENSE DISCLAIMER -------------------|
# |                                                                      |
# | Copyright (C) 2019  droxIT GmbH - devs@droxit.de                     |
# |                                                                      |
# | This file is part of ROXcomposer GUI.                                |
# |                                                                      |
# | ROXcomposer GUI is free software:                                    |
# | you can redistribute it and/or modify                                |
# | it under the terms of the GNU General Public License as published by |
# | the Free Software Foundation, either version 3 of the License, or    |
# | (at your option) any later version.                                  |
# |                                                                      |
# | This program is distributed in the hope that it will be useful,      |
# | but WITHOUT ANY WARRANTY; without even the implied warranty of       |
# | MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the         |
# | GNU General Public License for more details.                         |
# |                                                                      |
# | You have received a copy of the GNU General Public License           |
# | along with this program. See also <http://www.gnu.org/licenses/>.    |
# |                                                                      |
# |----------------------------------------------------------------------|
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
	span.style = "white-space: pre-wrap;" // this is essential to correctly show the /n newlines
	span.setAttribute("id", "log-" + id);
	let error_keywords = ["error", "fatal", "critical"]

	error_keywords.forEach((keyword)=>{
	    if(log.text.toLowerCase().includes(keyword))
	        span.setAttribute("class", "bold-red");
	});

	//span.setAttribute("style", "font-size:0.7em");
	make_logline_text(span, log);
	log_win.appendChild(span);
}

/* Create the text node for one log line. */
function make_logline_text(node, logline) {
	var br = document.createElement("br");
	// var log = logline.text.replace(/(?:\r\n|\r|\n)/g, '<br>');
	var log = escape_text(logline.text); // in roxgui/static/base/js/base_functions.js
	node.innerHTML = log;
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
function reload_logs() {
	// Update constantly reloaded elements.
	log_win = document.getElementById("log");
	update_log(log_win);
	setInterval(function() {
		update_log(log_win);
	}, 1000);
}


function clear_all(){
    
}