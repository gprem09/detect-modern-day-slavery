var map = L.map('map').setView([0, 0], 2);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

fetch('/static/dataset/GLAD_Confidence_Footprint.geojson')
  .then(response => response.json())
  .then(data => {
    L.geoJSON(data, {
      style: function (feature) {
        return {
          color: '#ff0000',  // Red borders
          weight: 0,         // Thickness of borders
          fillColor: '#ff9999',  // Light red fill color
          fillOpacity: 0.5   // Semi-transparent fill
        };
      },
      onEachFeature: function (feature, layer) {
        if (feature.properties) {
          layer.bindPopup(`<b>${feature.properties.NAME}</b>`); 
        }
      }
    }).addTo(map);
  })
  .catch(error => console.error('Error loading the GeoJSON:', error));
