// mapInit.js
let map;

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 46.2276, lng: 2.2137},
        zoom: 6,
        // Add custom map styles if needed
    });

    // Listener for map click
    // map.addListener('click', function(mapsMouseEvent) {
    //     const clickedLat = mapsMouseEvent.latLng.lat();
    //     const clickedLng = mapsMouseEvent.latLng.lng();
    //     getWeatherByCoords(clickedLat, clickedLng);
    // });

    map.addListener('click', function(mapsMouseEvent) {
        const clickedLat = mapsMouseEvent.latLng.lat();
        const clickedLng = mapsMouseEvent.latLng.lng();

        // Appel de la fonction qui gère le clic sur la ville
        onCityClick(clickedLat, clickedLng);
    });


    // Listener for zoom change
    map.addListener('zoom_changed', updateWeatherInfoOnZoom);
// Ajout de l'écouteur d'événements
map.addListener('idle', function() {
    // Fonction appelée à chaque fois que l'utilisateur finit de bouger la carte
    updateWeatherDataOnMap();
});
    // Additional initialization code...
}

google.maps.event.addDomListener(window, 'load', initMap);


