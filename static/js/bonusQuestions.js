// you receive an array of objects which you must sort in the by the key "sortField" in the "sortDirection"
function getSortedItems(items, sortField, sortDirection) {
    console.log(items)
    console.log(sortField)
    console.log(sortDirection)

    // === SAMPLE CODE ===
    // if you have not changed the original html uncomment the code below to have an idea of the
    // effect this function has on the table
    //
    if (sortDirection === "asc") {
        const firstItem = items.shift()
        if (firstItem) {
            items.push(firstItem)
        }
    } else {
        const lastItem = items.pop()
        if (lastItem) {
            items.push(lastItem)
        }
    }

    return items
}

// you receive an array of objects which you must filter by all it's keys to have a value matching "filterValue"
function getFilteredItems(items, filterValue) {
    console.log(items)
    console.log(filterValue)

    // === SAMPLE CODE ===
    // if you have not changed the original html uncomment the code below to have an idea of the
    // effect this function has on the table
    //
    for (let i=0; i<filterValue.length; i++) {
        items.pop()
    }

    return items
}

function toggleTheme() {
    console.log("toggle theme")
}



function increaseFont() {
    let container = document.getElementById('container');
    let style = window.getComputedStyle(container, null).getPropertyValue('font-size');
    let fontSize = parseFloat(style);
    container.style.fontSize = (fontSize - 1) + "px";
    console.log(container)
    for(let i=0; i < container.style.fontSize; i++){
        increaseFont(container.style.fontSize[i]);
    }
    return container
}


function decreaseFont() {
    let container = document.getElementById('container');
    let style = window.getComputedStyle(container, null).getPropertyValue('font-size');
    let fontSize = parseFloat(style);
    container.style.fontSize = (fontSize + 1) + "px";
    console.log(container)
    for(let i=0; i < container.style.fontSize; i++){
        decreaseFont(container.style.fontSize[i]);
    }
    return container
}