let map;
var autocomplete
function mapInit() {
    map = new google.maps.Map(document.getElementById('formMap'), {
        center: { lat: 44.9727, lng: -93.2354 },
        zoom: 14
    });
    map.addListener('click', handleMapClick);
    autocomplete = new google.maps.places.Autocomplete(document.getElementById('location'), { map, fields: ['name', 'geometry'], types: ['geocode'] });
    // document.getElementById('location').addEventListener('input', fillInAddress);
    autocomplete.addListener("place_changed",fillInAddress);
    
}
function fillInAddress() {

    const place = autocomplete.getPlace();

    if (place && place.geometry) {
        const location = place.geometry.location;

        const geocoder = new google.maps.Geocoder();
        geocoder.geocode({ location: location }, (results, status) => {
            if (status === 'OK' && results.length > 0) {
                const placeName = results[0].name;
                const formattedAddress = results[0].formatted_address;
                // Create a marker for the selected location
                const marker = new google.maps.Marker({
                    position: location,
                    map: map,
                    title: place.name
                });
                marker.addListener('click', () => {
                    const contentString = `<div><strong>${placeName}</strong><br>Address: ${formattedAddress}</div>`;
                    const infowindow = new google.maps.InfoWindow({ content: contentString });
                    infowindow.open(map, marker);
                });
                map.panTo(location);

                document.getElementById('location').value = formattedAddress;

            } else {
                console.error('Reverse geocoding failed with status: ' + status);
            }
        });
    }
}

function handleMapClick(event) {
    const clickedLocation = event.latLng;
    const geocoder = new google.maps.Geocoder();
    geocoder.geocode({ location: clickedLocation }, (results, status) => {
        if (status === 'OK' && results.length > 0) {
            const clickedAddress = results[0].formatted_address;

            document.getElementById('location').value = clickedAddress;
        } else {
            console.error('Reverse geocoding failed with status: ' + status);
        }
    });
}