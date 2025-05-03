from flask import Flask, request, jsonify, send_from_directory
import joblib
import numpy as np
import os
import json

# Set up paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "../model")
FRONTEND_DIR = os.path.join(BASE_DIR, "../frontend")
STATIC_DIR = os.path.join(FRONTEND_DIR, "static")

# Initialize Flask app
app = Flask(__name__, static_folder=STATIC_DIR)

# Load AI model and encoders
model = joblib.load(os.path.join(MODEL_DIR, "carbon_model.pkl"))
encoders = joblib.load(os.path.join(MODEL_DIR, "label_encoders.pkl"))

@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory(STATIC_DIR, path)

@app.route('/calculate', methods=['POST'])
@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        print("🧾 Received data:", data)

        categorical_fields = ['Heating Energy Source', 'Vehicle Type', 'Transport']
        numerical_fields = ['Monthly Grocery Bill', 'Vehicle Monthly Distance km',
                            'Waste Bag Weekly Count', 'How Long TV PC Daily Hour',
                            'How Many New Clothes Monthly', 'How Long Internet Daily Hour']

        processed_data = []
        for field in categorical_fields:
            le = encoders[field]
            processed_data.append(le.transform([data[field]])[0])

        for field in numerical_fields:
            processed_data.append(float(data[field]))

        X = np.array([processed_data])
        prediction = model.predict(X)[0]
        return jsonify({'total_emissions': round(prediction, 2)})

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
