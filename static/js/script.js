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
      },
      onEachFeature: function (feature, layer) {
        if (feature.properties) {
          layer.bindPopup(`<b>${feature.properties.NAME}</b>`); 
        }
        var seed = feature.properties.NAME || 'default-seed';
        var rng = new Math.seedrandom(seed);
        var randomPoints = generateRandomPointsInPolygon(feature, 20, rng);

        randomPoints.forEach(function(coords) {
          L.circleMarker([coords[1], coords[0]], {
            radius: 3,
            color: '#ff0000',
            fillColor: '#ff0000',
            fillOpacity: 1
          }).addTo(map);
        });
      }
    }).addTo(map);
  })
  .catch(error => console.error('Error loading the GeoJSON:', error));

function generateRandomPointsInPolygon(polygon, numPoints, rng) {
  var points = [];
  var bbox = turf.bbox(polygon);
  var minX = bbox[0];
  var minY = bbox[1];
  var maxX = bbox[2];
  var maxY = bbox[3];

  var attempts = 0;
  while (points.length < numPoints && attempts < numPoints * 10) {
    var x = minX + rng() * (maxX - minX);
    var y = minY + rng() * (maxY - minY);
    var point = turf.point([x, y]);
    if (turf.booleanPointInPolygon(point, polygon)) {
      points.push(point.geometry.coordinates);
    }
    attempts++;
  }

  return points;
}
