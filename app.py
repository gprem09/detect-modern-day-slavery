from flask import Flask, render_template, send_file
import folium
import os

app = Flask(__name__)

def generate_map():
    map_center = [0, 0]
    my_map = folium.Map(location=map_center, zoom_start=2)

    geojson_path = 'Deforestation_alerts_(RADD).geojson'

    folium.GeoJson(
        geojson_path,
        name='Deforestation Alerts',
        style_function=lambda x: {'color': 'red', 'fillOpacity': 0.5}
    ).add_to(my_map)

    my_map.save('map.html')

@app.route('/')
def index():
    generate_map()
    return render_template('index.html')

@app.route('/map')
def serve_map():
    map_path = os.path.join(os.getcwd(), 'map.html') 
    return send_file(map_path) 

if __name__ == '__main__':
    app.run(debug=True)
