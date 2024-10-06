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
          color: '#ff0000',
          weight: 0,
          fillColor: '#ff9999',
          fillOpacity: 0
        };
      }
    }).addTo(map);
  })
  .catch(error => console.error('Error loading the GeoJSON:', error));

fetch('/get_illegal_points')
  .then(response => response.json())
  .then(points => {
    if (points.error) {
      console.error("Error from server:", points.error);
      alert("No illegal deforestation points found.");
      return;
    }

    points.forEach(function(coords) {
      L.circleMarker([coords[0], coords[1]], {
        radius: 0.5,
        color: '#FF0000',
        fillColor: '#FF0000',
        fillOpacity: 1
      }).addTo(map);
    });
  })
  .catch(error => console.error('Error loading classified points:', error));
