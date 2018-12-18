function refresh() {
	setTimeout(function() {
		location.reload()
	}, 100);
}

// Update constantly reloaded elements.
acc = document.getElementById("accordion");
log_win = document.getElementById("log");
setInterval(function() {
	get_msg_status(acc);
	update_log(log_win);
}, 1000);
