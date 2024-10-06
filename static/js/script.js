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
          weight: 1, // Outline the polygons
          fillColor: '#ff9999',
          fillOpacity: 0 // Make fill transparent
        };
      },
      onEachFeature: function (feature, layer) {
        if (feature.properties) {
          layer.bindPopup(`<b>${feature.properties.NAME}</b>`); 
        }

        // Set the seed based on the polygon's NAME or a default value
        var seed = feature.properties.NAME || 'default-seed';
        // Initialize the seeded random number generator
        var rng = new Math.seedrandom(seed);

        // Generate random points within the polygon
        var randomPoints = generateRandomPointsInPolygon(feature, 20, rng); // Adjust the number of points as needed

        // Add circle markers for each random point
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

// Function to generate random points within a polygon using a seeded RNG
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
