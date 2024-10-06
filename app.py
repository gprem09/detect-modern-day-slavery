from flask import Flask, render_template, jsonify
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon, MultiPolygon

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def classify_points():
    try:
        df = pd.read_csv('static/dataset/illegal_deforestation.csv')
        coordinates = df[['latitude', 'longitude']].values

        geojson = gpd.read_file('static/dataset/GLAD_Confidence_Footprint.geojson')
        if geojson.crs != 'EPSG:4326':
            geojson = geojson.to_crs(epsg=4326)

        points_inside_polygons = []
        for coord in coordinates:
            point = Point(coord[1], coord[0])
            for geom in geojson['geometry']:
                if isinstance(geom, Polygon):
                    if geom.contains(point):
                        points_inside_polygons.append([coord[0], coord[1]])
                        break
                elif isinstance(geom, MultiPolygon):
                    for poly in geom.geoms:
                        if poly.contains(point):
                            points_inside_polygons.append([coord[0], coord[1]])
                            break

        return points_inside_polygons

    except Exception as e:
        print(f"Error during classification: {e}")
        return []

@app.route('/get_illegal_points', methods=['GET'])
def get_illegal_points():
    points = classify_points()
    if points:
        return jsonify(points)
    else:
        return jsonify({"error": "No points found"}), 500

if __name__ == '__main__':
    app.run(debug=True)
