// markerCluster.js
function createMarkerCluster(markers) {
    new MarkerClusterer(map, markers, { imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m' });
}

// Call this function in mapInit.js or where you create markers
