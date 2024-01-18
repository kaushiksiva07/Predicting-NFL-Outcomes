// nflpreds.js
function weekSelected() {
    var test = 1
    var week = document.getElementById("weekDropdown").value;
    if (week) {
        fetch(`/load_week_data/${week}`)
            .then(response => response.text())
            .then(data => {
                document.getElementById("dataContainer").innerHTML = data;
            });
    }
    
}
