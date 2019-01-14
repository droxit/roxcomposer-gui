function filter(filterList, condition) {
    return filterList.filter(condition);
}

function sort(sortList, condition) {
    return sortList.sort(condition);
}

function search(searchList, item) {
    // returns a list of elements matching the item
    return filter(searchList, function(itemInList){
        return itemInList.includes(item);
    });

}

function sortByAlphabet(sortList){
    return sort(sortList, function(a, b){
        if(a < b) {return -1; }
        if(a > b) {return 1; }
        return 0;
    });
}

