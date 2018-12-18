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

document.addEventListener('DOMContentLoaded', function () {

  //
  // Initialize stuff
  //

  var grid = null;
  var docElem = document.documentElement;
  var demo = document.querySelector('.grid-demo');
  var gridElement = demo.querySelector('.grid');
  var filterField = demo.querySelector('.filter-field');
  var searchField = demo.querySelector('.search-field');
  var sortField = demo.querySelector('.sort-field');
  var layoutField = demo.querySelector('.layout-field');
  var addItemsElement = demo.querySelector('.add-more-items');
  var characters = 'abcdefghijklmnopqrstuvwxyz';
  var filterOptions = ['red', 'blue', 'green'];
  var dragOrder = [];
  var uuid = 0;
  var filterFieldValue;
  var sortFieldValue;
  var layoutFieldValue;
  var searchFieldValue;

  var grid2 = null;
  var grid2Hash = {};
  var demo2 = document.querySelector('.grid-demo2');
  var gridElement2 = demo2.querySelector('.grid2');

  //
  // Grid helper functions
  //

  function initDemo() {

    initGrid();
    initGrid2();

    // Reset field values.
    searchField.value = '';
    [sortField, filterField, layoutField].forEach(function (field) {
      field.value = field.querySelectorAll('option')[0].value;
    });

    // Set inital search query, active filter, active sort value and active layout.
    searchFieldValue = searchField.value.toLowerCase();
    filterFieldValue = filterField.value;
    sortFieldValue = sortField.value;
    layoutFieldValue = layoutField.value;

    // Search field binding.
    searchField.addEventListener('keyup', function () {
      var newSearch = searchField.value.toLowerCase();
      if (searchFieldValue !== newSearch) {
        searchFieldValue = newSearch;
        filter();
      }
    });

    // Filter, sort and layout bindings.
    filterField.addEventListener('change', filter);
    sortField.addEventListener('change', sort);
    layoutField.addEventListener('change', changeLayout);

    // Add/remove items bindings.
    addItemsElement.addEventListener('click', addItems);
    gridElement.addEventListener('click', function (e) {
      if (elementMatches(e.target, '.mcard-remove, .mcard-remove i')) {
        removeItem(e);
      }
    });
    gridElement2.addEventListener('click', function (e) {
      if (elementMatches(e.target, '.mcard-remove, .mcard-remove i')) {
        removeItem(e);
      }
    });

  }

  function initGrid2() {

    var dragCounter = 0;

    grid2 = new Muuri(gridElement2, {
      items: generateElements(2),
      layoutDuration: 400,
      layoutEasing: 'ease',
      dragEnabled: true,
      dragSort: getAllGrids,
      dragSortInterval: 50,
      dragContainer: document.body,
      dragStartPredicate: function (item, event) {
        var isDraggable = sortFieldValue === 'order';
        var isRemoveAction = elementMatches(event.target, '.mcard-remove, .mcard-remove i');
        return isDraggable && !isRemoveAction ? Muuri.ItemDrag.defaultStartPredicate(item, event) : false;
      },
      dragReleaseDuration: 400,
      dragReleseEasing: 'ease'
    })
    .on('dragStart', function () {
      ++dragCounter;
      docElem.classList.add('dragging');
    })
    .on('dragEnd', function () {
      if (--dragCounter < 1) {
        docElem.classList.remove('dragging');
      }
    })
    .on('move', updateIndices)
    .on('sort', updateIndices)
    .on('receive', function (data) {
      grid2Hash[data.item._id] = function (item) {
        if (item === data.item) {
          var clone = cloneElem(data.item.getElement());
          data.fromGrid.add(clone, {index: data.fromIndex});
          data.fromGrid.show(clone);
        }
      };
      grid2.once('dragReleaseStart', grid2Hash[data.item._id]);
      //elem2to1(data);
    })
    .on('send', function (data) {
      var listener = grid2Hash[data.item._id];
      if (listener) {
        grid2.off('dragReleaseStart', listener);
      }
    });

  }

  function elem2to1(data){
      var cl = data.item.getElement().getAttribute('class');
      var new_str = cl.replaceAt(5, 'h1');
      data.item.getElement().setAttribute('class', new_str);
  }

  function cloneElem(elem) {
      var clone = elem.cloneNode(true);
      var cl = elem.getAttribute('class');
      var new_str = cl.replaceAt(5, 'h1');
      elem.setAttribute('class', new_str);
      //clone.setAttribute('style', 'display:none;');
      //clone.setAttribute('class', 'item');
      //clone.children[0].setAttribute('style', '');
      return clone;
    }

  String.prototype.replaceAt=function(index, replacement) {
    return this.substr(0, index) + replacement+ this.substr(index + replacement.length);
  }

  function initGrid() {

    var dragCounter = 0;

    grid = new Muuri(gridElement, {
      items: generateElements(5),
      layoutDuration: 400,
      layoutEasing: 'ease',
      dragEnabled: true,
      dragSort: getAllGrids,
      dragSortInterval: 50,
      dragContainer: document.body,
      dragStartPredicate: function (item, event) {
        var isDraggable = sortFieldValue === 'order';
        var isRemoveAction = elementMatches(event.target, '.mcard-remove, .mcard-remove i');
        return isDraggable && !isRemoveAction ? Muuri.ItemDrag.defaultStartPredicate(item, event) : false;
      },
      dragReleaseDuration: 400,
      dragReleseEasing: 'ease'
    })
    .on('dragStart', function () {
      ++dragCounter;
      docElem.classList.add('dragging');
    })
    .on('dragEnd', function () {
      if (--dragCounter < 1) {
        docElem.classList.remove('dragging');
      }
    })
    .on('move', updateIndices)
    .on('sort', updateIndices);

  }

  function filter() {

    filterFieldValue = filterField.value;
    grid.filter(function (item) {
      var element = item.getElement();
      var isSearchMatch = !searchFieldValue ? true : (element.getAttribute('data-title') || '').toLowerCase().indexOf(searchFieldValue) > -1;
      var isFilterMatch = !filterFieldValue ? true : (element.getAttribute('data-color') || '') === filterFieldValue;
      return isSearchMatch && isFilterMatch;
    });

  }

  function sort() {

    // Do nothing if sort value did not change.
    var currentSort = sortField.value;
    if (sortFieldValue === currentSort) {
      return;
    }

    // If we are changing from "order" sorting to something else
    // let's store the drag order.
    if (sortFieldValue === 'order') {
      dragOrder = grid.getItems();
    }

    // Sort the items.
    grid.sort(
      currentSort === 'title' ? compareItemTitle :
      currentSort === 'color' ? compareItemColor :
      dragOrder
    );

    // Update indices and active sort value.
    updateIndices();
    sortFieldValue = currentSort;

  }

  function addItems() {

    // Generate new elements.
    var newElems = generateElements(5);

    // Set the display of the new elements to "none" so it will be hidden by
    // default.
    newElems.forEach(function (item) {
      item.style.display = 'none';
    });

    // Add the elements to the grid.
    var newItems = grid.add(newElems);

    // Update UI indices.
    updateIndices();

    // Sort the items only if the drag sorting is not active.
    if (sortFieldValue !== 'order') {
      grid.sort(sortFieldValue === 'title' ? compareItemTitle : compareItemColor);
      dragOrder = dragOrder.concat(newItems);
    }

    // Finally filter the items.
    filter();

  }

  function removeItem(e) {

    var elem = elementClosest(e.target, '.item');
    grid.hide(elem, {onFinish: function (items) {
      var item = items[0];
      grid.remove(item, {removeElements: true});
      if (sortFieldValue !== 'order') {
        var itemIndex = dragOrder.indexOf(item);
        if (itemIndex > -1) {
          dragOrder.splice(itemIndex, 1);
        }
      }
    }});
    updateIndices();

  }

  function changeLayout() {

    layoutFieldValue = layoutField.value;
    grid._settings.layout = {
      horizontal: false,
      alignRight: layoutFieldValue.indexOf('right') > -1,
      alignBottom: layoutFieldValue.indexOf('bottom') > -1,
      fillGaps: layoutFieldValue.indexOf('fillgaps') > -1
    };
    grid.layout();

  }

  //
  // Generic helper functions
  //

  function generateElements(amount) {

    var ret = [];

    for (var i = 0, len = amount || 1; i < amount; i++) {

      var id = ++uuid;
      var color = getRandomItem(filterOptions);
      var title = generateRandomWord(20);
      var width = 2;
      var height = Math.floor(Math.random() * 2) + 1;
      var itemElem = document.createElement('div');
      var itemTemplate = '' +
          '<div class="item h' + height + ' w' + width + ' ' + color + '" data-id="' + id + '" data-color="' + color + '" data-title="' + title + '">' +
            '<div class="item-content">' +
              '<div class="mcard">' +
                '<div class="mcard-id">' + id + '</div>' +
                '<div class="mcard-title"> <span style="display:block;word-wrap:break-word;line-height:30px"> <br>' + title + '</span></div>' +
                '<div class="mcard-remove"><i class="material-icons">&#xE5CD;</i></div>' +
              '</div>' +
            '</div>' +
          '</div>';

      itemElem.innerHTML = itemTemplate;
      ret.push(itemElem.firstChild);

    }

    return ret;

  }

  function getAllGrids(){
    return [grid, grid2];
  }

  function getRandomFloat(wordlength) {
      return Math.floor(Math.random() * wordlength/100);
    }

  function getRandomItem(collection) {

    return collection[Math.floor(Math.random() * collection.length)];

  }

  function generateRandomWord(length) {

    var ret = '';
    for (var i = 0; i < length; i++) {
      ret += getRandomItem(characters);
    }
    return ret;

  }

  function compareItemTitle(a, b) {

    var aVal = a.getElement().getAttribute('data-title') || '';
    var bVal = b.getElement().getAttribute('data-title') || '';
    return aVal < bVal ? -1 : aVal > bVal ? 1 : 0;

  }

  function compareItemColor(a, b) {

    var aVal = a.getElement().getAttribute('data-color') || '';
    var bVal = b.getElement().getAttribute('data-color') || '';
    return aVal < bVal ? -1 : aVal > bVal ? 1 : compareItemTitle(a, b);

  }

  function updateIndices() {

    var grids = getAllGrids();
    grids.forEach(function(grid_elem, j){
        grid_elem.getItems().forEach(function (item, i) {
          item.getElement().setAttribute('data-id', i + 1);
          item.getElement().querySelector('.mcard-id').innerHTML = i + 1;
        });
    });

  }

  function elementMatches(element, selector) {

    var p = Element.prototype;
    return (p.matches || p.matchesSelector || p.webkitMatchesSelector || p.mozMatchesSelector || p.msMatchesSelector || p.oMatchesSelector).call(element, selector);

  }

  function elementClosest(element, selector) {

    if (window.Element && !Element.prototype.closest) {
      var isMatch = elementMatches(element, selector);
      while (!isMatch && element && element !== document) {
        element = element.parentNode;
        isMatch = element && element !== document && elementMatches(element, selector);
      }
      return element && element !== document ? element : null;
    }
    else {
      return element.closest(selector);
    }

  }

  //
  // Fire it up!
  //

  initDemo();

});