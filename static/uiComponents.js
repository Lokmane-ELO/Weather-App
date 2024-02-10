// Assuming this global variable is set in mapInit.js
//let map; 

// Initialize a single InfoWindow to be reused
let infowindow = new google.maps.InfoWindow();

/**
 * Updates the content and position of the InfoWindow.
 * @param {string} content - HTML content to display inside the InfoWindow.
 * @param {google.maps.LatLng} position - The position to anchor the InfoWindow.
 */
function updateInfoWindow(content, position) {
    infowindow.setContent(content);
    infowindow.setPosition(position);
    infowindow.open(map);
}

/**
 * Shows or hides a loading indicator.
 * @param {boolean} show - Whether to show or hide the loading indicator.
 */
function showLoadingIndicator(show) {
    const loadingIndicator = document.getElementById('loadingIndicator');
    if (show) {
        loadingIndicator.style.display = 'block';
    } else {
        loadingIndicator.style.display = 'none';
    }
}

/**
 * Creates and adds a legend to the map.
 */
function createLegend() {
    const legend = document.createElement('div');
    legend.id = 'legend';
    legend.innerHTML = `
        <h3>Temperature Legend</h3>
        <p><span class="legend-color" style="background: red;"></span> > 25°C</p>
        <p><span class="legend-color" style="background: orange;"></span> 15°C - 25°C</p>
        <p><span class="legend-color" style="background: blue;"></span> < 15°C</p>
    `;
    legend.classList.add('legend');
    map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(legend);
}

// Add this in your CSS
// .legend { background: white; padding: 10px; margin: 10px; border: 1px solid #000; }
// .legend-color { width: 15px; height: 15px; display: inline-block; margin-right: 5px; }
// #loadingIndicator { /* Your loading indicator styles */ }

// Call these functions in mapInit.js after the map is initialized
// createLegend();
// showLoadingIndicator(true or false);

// function createWeatherMarker(location, weatherData, type) {
//     let marker = new google.maps.Marker({
//         position: { lat: location.lat, lng: location.lng },
//         map: map,
//         // Customize marker based on weatherData and type (region/city)
//     });

//     // Optionally, add a click listener to show detailed weather in an InfoWindow
// }


