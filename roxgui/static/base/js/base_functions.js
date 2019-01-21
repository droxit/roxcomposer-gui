/* Search for keywords in list of strings. */
function keyword_search(search_list, item) {
	if (search_list != null && item != null && item != "") {
		return search_list.filter(function(list_item) {
			return list_item.includes(item);
		});
	} else {
		return [];
	}
}

/* Search for keywords in custom data structure. */
function custom_keyword_search(search_list, item, condition) {
	if (search_list != null && item != null && item != "" && condition != null) {
	    result_list = [];
	    search_list.forEach(function(container) {
	        if (condition(container, item)) {
	            result_list.push(container);
	        }
	    })
	    return result_list;
	} else {
	    return [];
	}
}

/* Sort given list of numbers or strings in alphabetical order. */
function alphabetical_sort(sort_list) {
	if (sort_list != null) {
		return sort_list.sort(function(a, b) {
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

/* Convert JSON instance to properly formatted string. */
function convert_to_json_string(json_instance) {
    json_string = JSON.stringify(json_instance, null, '\t');
    return json_string;
}
