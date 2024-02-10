/**
 * Fetches weather data for a specific latitude and longitude.
 * @param {number} lat - Latitude.
 * @param {number} lng - Longitude.
 */

function getWeatherByCoords(lat, lng) {
    const url = `/get_weather_by_coords?lat=${lat}&lon=${lng}`;
    return fetch(url) // Retourne la promesse ici
        .then(response => response.json())
        .then(data => {
            if (data && data.main && data.name) {
                // Update InfoWindow content and position
                updateInfoWindow(`City: ${data.name}, Temp: ${data.main.temp}°C`, {lat, lng});
                return data; // Retourne les données pour la chaîne de promesses
            }
        })
        .catch(error => {
            console.error('Error fetching weather data:', error);
            // Handle error (e.g., show error message to user)
        });
}
/**
 * Fetches weather data based on the current map zoom level and bounds.
 * This function is called when the map's zoom level changes.
 */


function updateWeatherInfoOnZoom() {
    const zoomLevel = map.getZoom();
    const bounds = map.getBounds();
    const NE = bounds.getNorthEast();
    const SW = bounds.getSouthWest();

    // Adjust these URLs to point to your Flask backend routes
    const url = zoomLevel > 8 
        ? `/get_weather_by_coords?lat=${NE.lat()}&lon=${NE.lng()}` 
        : `/get_regional_weather?lat=${NE.lat()}&lon=${NE.lng()}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data && data.main) {
                // Process data and update the map (e.g., create or update circles)
                // Consider creating a separate function for handling this
            }
        })
        .catch(error => console.error('Error fetching weather data:', error));
}

// function displayRegionalWeather() {
//     // Define regions with their coordinates
//     const regions = [/* Array of regions with lat, lon */];

//     regions.forEach(region => {
//         const url = `/get_weather_by_coords?lat=${region.lat}&lon=${region.lon}`;
//         fetch(url)
//             .then(response => response.json())
//             .then(data => {
//                 createWeatherMarker(region, data, 'region'); // Create regional markers
//             })
//             .catch(error => console.error('Error:', error));
//     });
// }

function onCityClick(lat, lng, cityName) {
    // Premier appel pour obtenir les données météo
    getWeatherByCoords(lat, lng)
        .then(weatherData => {
            let content = `City: ${weatherData.name}, Temp: ${weatherData.main.temp}°C`;

            // Deuxième appel pour obtenir une image de la ville
            getCityImage(weatherData.name)
                .then(imageUrl => {
                    content += `<img src="${imageUrl}" alt="Photo of ${cityName}" style="width:100%; max-height:200px;">`;
                    updateInfoWindow(content, {lat: lat, lng: lng});
                })
                .catch(error => console.error('Error fetching city image:', error));
        })
        .catch(error => {
            console.error('Error fetching weather data:', error);
        });
}

function getCityImage(cityName) {
    //console.log(cityName);
    const url = `https://api.unsplash.com/search/photos?query=${encodeURIComponent(cityName)}&client_id=YHNgVj-Ik08ek3kiVo1BJtz_PP6kkwSKhfoKjTWRg_Y`;
    //console.log(url);
    return fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.results && data.results.length > 0) {
                //console.log(data.results[0].urls.small);
                return data.results[0].urls.small; // Utiliser l'URL 'small' pour une meilleure performance
            } else {
                throw new Error('No image found');
            }
        });
}

document.getElementById('search-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const cityName = document.getElementById('city-search').value;
    if (cityName) {
        searchCity(cityName);
    }
});

function searchCity(cityName) {
    const openWeatherApiKey = 'b1fd6e14799699504191b6bdbcadfc35';
    const url = `https://api.openweathermap.org/data/2.5/weather?q=${encodeURIComponent(cityName)}&appid=${openWeatherApiKey}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data && data.coord) {
                // Utilisez les coordonnées de la ville pour mettre à jour la carte
                const lat = data.coord.lat;
                const lon = data.coord.lon;
                updateMap(lat, lon, cityName);
            } else {
                console.error('City not found');
            }
        })
        .catch(error => {
            console.error('Error fetching location data:', error);
        });
}

function updateMap(lat, lon, cityName) {
    map.setCenter({lat: lat, lng: lon});
    map.setZoom(10);  // Ajustez le niveau de zoom selon vos besoins

    onCityClick(lat, lon, cityName);
}



// function updateWeatherDataOnMap() {
//     const bounds = map.getBounds();
//     const NE = bounds.getNorthEast();
//     const SW = bounds.getSouthWest();

//     // Exemple : récupération des données pour les coins Nord-Est et Sud-Ouest
//     // Vous pouvez affiner cette logique pour cibler des villes spécifiques
//     getWeatherData(NE.lat(), NE.lng());
//     getWeatherData(SW.lat(), SW.lng());
// }

function getWeatherData(lat, lon) {
    const openWeatherApiKey = 'b1fd6e14799699504191b6bdbcadfc35';
    const url = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${openWeatherApiKey}&units=metric`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data) {
                displayWeatherOnMap(data);
            }
        })
        .catch(error => console.error('Error fetching weather data:', error));
}

function displayWeatherOnMap(weatherData) {
    const position = { lat: weatherData.coord.lat, lng: weatherData.coord.lon };
    const temp = weatherData.main.temp;
    const city = weatherData.name;

    const contentString = `<div><h3>${city}</h3><p>Température: ${temp} °C</p></div>`;

    const infowindow = new google.maps.InfoWindow({
        content: contentString
    });

    const marker = new google.maps.Marker({
        position: position,
        map: map,
        title: city
    });

    marker.addListener('click', function() {
        infowindow.open(map, marker);
    });
}
