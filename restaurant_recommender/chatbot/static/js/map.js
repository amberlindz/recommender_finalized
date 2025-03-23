// Initialize the map
let map = L.map('map').setView([34.0522, -118.2437], 11);

// Add the base map layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Store restaurant markers
let markers = [];
let restaurants = [];

// Fetch restaurant data and populate map
function loadRestaurants() {
    fetch('/api/restaurants/')
        .then(response => response.json())
        .then(data => {
            restaurants = data;
            
            // Add markers for each restaurant
            restaurants.forEach(restaurant => {
                // Geocode the address (in a real implementation, coordinates would be in the JSON)
                fetch(`/api/geocode/?address=${encodeURIComponent(restaurant.address)}`)
                    .then(response => response.json())
                    .then(coords => {
                        if (coords.lat && coords.lng) {
                            // Create marker
                            let marker = L.marker([coords.lat, coords.lng])
                                .addTo(map)
                                .bindPopup(`
                                    <strong>${restaurant.name}</strong><br>
                                    ${restaurant.address}<br>
                                    <a href="${restaurant.website}" target="_blank">Website</a>
                                `);
                            
                            markers.push({
                                marker: marker,
                                neighborhood: restaurant.neighborhood,
                                restaurantId: restaurant.id
                            });
                        }
                    });
            });
            
            // Populate neighborhood filter
            const neighborhoodSelect = document.getElementById('neighborhood-filter');
            const neighborhoods = [...new Set(restaurants.map(r => r.neighborhood))].sort();
            
            neighborhoods.forEach(neighborhood => {
                const option = document.createElement('option');
                option.value = neighborhood;
                option.textContent = neighborhood;
                neighborhoodSelect.appendChild(option);
            });
        });
}

// Filter markers by neighborhood
document.getElementById('neighborhood-filter').addEventListener('change', function() {
    const selectedNeighborhood = this.value;
    
    markers.forEach(item => {
        if (!selectedNeighborhood || item.neighborhood === selectedNeighborhood) {
            map.addLayer(item.marker);
        } else {
            map.removeLayer(item.marker);
        }
    });
});

// Highlight recommended restaurants
function highlightRestaurants(restaurantIds) {
    // Reset all markers to default
    markers.forEach(item => {
        item.marker.setIcon(L.icon({
            iconUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png',
            iconSize: [25, 41],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
            shadowUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png',
            shadowSize: [41, 41],
            shadowAnchor: [12, 41]
        }));
    });
    
    // Highlight recommended restaurants
    markers.filter(item => restaurantIds.includes(item.restaurantId))
        .forEach(item => {
            item.marker.setIcon(L.icon({
                iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
                iconSize: [25, 41],
                iconAnchor: [12, 41],
                popupAnchor: [1, -34],
                shadowUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png',
                shadowSize: [41, 41],
                shadowAnchor: [12, 41]
            }));
            
            // Open popup for the first recommendation
            if (restaurantIds.indexOf(item.restaurantId) === 0) {
                item.marker.openPopup();
                
                // Center map on the first recommendation
                map.setView(item.marker.getLatLng(), 14);
            }
        });
}

// Mobile sidebar toggle
document.getElementById('toggle-sidebar').addEventListener('click', function() {
    document.getElementById('sidebar').classList.add('active');
});

document.getElementById('close-sidebar').addEventListener('click', function() {
    document.getElementById('sidebar').classList.remove('active');
});

// Load restaurants when the page loads
document.addEventListener('DOMContentLoaded', loadRestaurants);