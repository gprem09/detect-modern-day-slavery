from flask import Flask, render_template, jsonify
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model

app = Flask(__name__)

def load_nn_model():
    try:
        model = load_model('mlp_model.h5')
        print("Neural Network model loaded successfully.")
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None
def classify_points_with_nn(model):
    try:
        df = pd.read_csv('static/dataset/illegal_deforestation.csv')
        coordinates = df[['latitude', 'longitude']].values
        predictions = model.predict(coordinates)
        illegal_points = coordinates[predictions.flatten() > 0.5]
        points_inside_polygons = illegal_points.tolist()

        return points_inside_polygons
    except Exception as e:
        print(f"Error during classification: {e}")
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_illegal_points', methods=['GET'])
def get_illegal_points():
    model = load_nn_model()

    if model is not None:
        points = classify_points_with_nn(model)
        if points:
            return jsonify(points)
        else:
            return jsonify({"error": "No illegal points found"}), 500
    else:
        return jsonify({"error": "Model could not be loaded"}), 500

if __name__ == '__main__':
    app.run(debug=True)
