function filter(filterList, condition) {
    return filterList.filter(condition);
}

function sort() {

}

function search(searchList, item) {
    // returns a list of elements matching the item
    return filter(searchList, function(itemInList){
        return item == itemInList;
    });
}