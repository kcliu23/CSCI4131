// Declare variables
let markers = [];
let map;

// Event listeners
document.getElementById("myButton").addEventListener("click", searchPlaces);
document.getElementById("place-type").addEventListener("change", toggleKeywordTextbox);
document.getElementById("Gobutton").addEventListener("click", calculateAndDisplayRoute);

// Initialize map
function initMap() {
    map = new google.maps.Map(document.getElementById('map'), { center: { lat: 44.9727, lng: -93.2354 }, zoom: 14 });
    fetchAndGeocodeScheduleRows();
}

// Geocode location function
function geocodeLocation(geocoder, map, uniqueLocations, day, eventName, time, location) {
    geocoder.geocode({ address: location }, (results, status) => {
        if (status === 'OK' && results.length > 0) {
            const locationKey = results[0].geometry.location.toString();
            const customIcon = { url: '../img/Goldy.png', scaledSize: new google.maps.Size(40, 40) };
            uniqueLocations[locationKey] = uniqueLocations[locationKey] || [];
            uniqueLocations[locationKey].push({ day, eventName, time });

            if (uniqueLocations[locationKey].length >= 1) {
                const marker = new google.maps.Marker({ icon: customIcon, position: results[0].geometry.location, map, title: `${eventName} - ${time}` });
                const contentString = `<div><strong>${eventName}</strong><br>Day: ${generateRecurringEventList(uniqueLocations[locationKey])}Time: ${time}<br>Location: ${location}</div>`;
                const infowindow = new google.maps.InfoWindow({ content: contentString });

                marker.addListener('click', () => { infowindow.open(map, marker); });
                markers.push(marker);
            }
        } else {
            console.error('Geocoding failed for location: ' + location);
        }
    });
}

// Generate recurring event list
function generateRecurringEventList(events) {
    return '<ul>' + events.map(event => `<li>${event.day} - ${event.time}</li>`).join('') + '</ul>';
}

// Fetch and geocode schedule rows
function fetchAndGeocodeScheduleRows() {
    const scheduleRows = Array.from(document.querySelectorAll('.schedule-table tbody tr')).slice(1);
    const uniqueLocations = {};

    scheduleRows.forEach(row => {
        const [day, eventName, time, location] = row.cells;
        const formattedLocation = (location.innerText === "Remote Class") ? "Centennial Hall, 614 Delaware St SE, Minneapolis, MN 55455" : location.innerText;
        geocodeLocation(new google.maps.Geocoder(), map, uniqueLocations, day.innerText, eventName.innerText, time.innerText, formattedLocation);
    });
}

// Create marker for place
function createMarkerForPlace(place) {
    const marker = new google.maps.Marker({ map, position: place.geometry.location, title: place.name });

    marker.addListener('click', () => {
        const contentString = `<div><strong>${place.name}</strong><br>Address: ${place.vicinity}</div>`;
        const infowindow = new google.maps.InfoWindow({ content: contentString });
        infowindow.open(map, marker);
    });

    markers.push(marker);
}

// Clear markers
function clearMarkers() {
    markers.forEach(marker => marker.setMap(null));
    markers = [];
}

// Search places function
function searchPlaces() {
    map = new google.maps.Map(document.getElementById('map'), { center: { lat: 44.9727, lng: -93.2354 }, zoom: 14 });
    const selectedType = document.getElementById('place-type').value;
    const radius = document.getElementById('radius').value;
    const center = map.getCenter();
    const directionsPanel = document.getElementById('directionsPanel');
    directionsPanel.style.display = 'none';
    const keywords = (selectedType.toLowerCase() === "other") ? document.getElementById('keywords').value : "";

    const request = { location: { lat: center.lat(), lng: center.lng() }, radius: parseInt(radius), type: selectedType, keyword: keywords };
    const placesService = new google.maps.places.PlacesService(map);

    if (selectedType !== "class") {
        placesService.nearbySearch(request, (results, status) => {
            if (status === google.maps.places.PlacesServiceStatus.OK) {
                clearMarkers();
                results.forEach(result => createMarkerForPlace(result));
            } else if (status === google.maps.places.PlacesServiceStatus.ZERO_RESULTS) {
                console.log('No places found for the given criteria.');
                alert('No places found for the given criteria.');
            } else {
                console.error('Places API search failed with status: ' + status);
            }
        });
    } else {
        clearMarkers();
        fetchAndGeocodeScheduleRows();
    }
}

// Toggle keyword textbox
function toggleKeywordTextbox() {
    const keywordsInput = document.getElementById('keywords');
    keywordsInput.disabled = (document.getElementById('place-type').value.toLowerCase() !== "other");
    if (document.getElementById('place-type').value !== 'other') {
        keywordsInput.value = "";
        keywordsInput.disabled = true;
    }
}

// Direction panel function
function calculateAndDisplayRoute() {
    map = new google.maps.Map(document.getElementById('map'), { center: { lat: 44.9727, lng: -93.2354 }, zoom: 14 });
    
    clearMarkers();
    
    const destination = document.getElementById('destination').value;
    const travelMode = document.querySelector('input[name="travelMode"]:checked').value;

    const directionsPanel = document.getElementById('directionsPanel');
    directionsPanel.style.display = 'block';

    const directionsService = new google.maps.DirectionsService();
    const directionsRenderer = new google.maps.DirectionsRenderer();
    
    directionsRenderer.setMap(map);
    directionsRenderer.setPanel(document.getElementById('directionsPanel'));

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(position => {
            const userLocation = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
            const placesService = new google.maps.places.PlacesService(map);

            placesService.textSearch({
                query: destination,
                bounds: map.getBounds(),
            }, (results, status) => {
                if (status == google.maps.places.PlacesServiceStatus.OK && results.length > 0) {
                    const destinationLocation = results[0].geometry.location;

                    const request = {
                        origin: userLocation,
                        destination: destinationLocation,
                        travelMode: travelMode
                    };

                    directionsService.route(request, (result, status) => {
                        if (status == 'OK') {
                            directionsRenderer.setDirections(result);
                        } else {
                            console.error('Error fetching directions: ' + status);
                        }
                    });
                } else {
                    console.error('Error searching for destination: ' + status);
                }
            });
        }, () => {
            console.error('Error getting user location.');
        });
    } else {
        console.error('Geolocation is not supported by this browser.');
    }
}
