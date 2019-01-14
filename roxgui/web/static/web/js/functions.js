function custom_filter(filterList, condition) {
	if (filterList != null && condition != null) {
		return filterList.filter(condition);
	} else {
		return [];
	}
}

function search(searchList, item) {
	if (searchList != null && item != null && item != "") {
		return custom_filter(searchList, function(itemInList) {
			return itemInList.includes(item);
		});
	} else {
		return [];
	}
}

function sort(sortList, condition) {
	if (sortList != null && condition != null) {
		return sortList.sort(condition);
	} else {
		return [];
	}
}

function alphabetical_sort(sortList) {
	if (sortList != null) {
		return sort(sortList, function(a, b) {
			if (a < b) {
				return -1;
			}
			if (a > b) {
				return 1;
			}
			return 0;
		});
	} else {
		return [];
	}
}
