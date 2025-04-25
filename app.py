import joblib
import numpy as np
from config.paths_config import MODEL_OUTPUT_PATH
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

loaded_model = joblib.load(MODEL_OUTPUT_PATH)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the input values from the form
        lead_time = int(request.form['lead_time'])
        no_of_special_requests = int(request.form['no_of_special_requests'])
        avg_price_per_room = float(request.form['avg_price_per_room'])
        arrival_month = int(request.form['arrival_month'])
        arrival_date = int(request.form['arrival_date'])
        market_segment_type = int(request.form['market_segment_type'])
        no_of_week_nights = int(request.form['no_of_week_nights'])
        no_of_weekend_nights = int(request.form['no_of_weekend_nights'])
        type_of_meal_plan = int(request.form['type_of_meal_plan'])
        room_type_reserved = int(request.form['room_type_reserved'])

        # Convert the input values to a numpy array
        features = np.array([[lead_time, no_of_special_requests, avg_price_per_room,
                             arrival_month, arrival_date, market_segment_type,
                             no_of_week_nights, no_of_weekend_nights,
                             type_of_meal_plan, room_type_reserved]])
        
        # Make a prediction using the loaded model
        prediction = loaded_model.predict(features)
        
        # Render the result template with the prediction
        return render_template('index.html', prediction=prediction[0])    
    
    return render_template('index.html', prediction=None)

@app.route('/api/predict', methods=['POST'])
def predict_api():
    """API endpoint for AJAX requests if needed in the future"""
    try:
        data = request.get_json()
        
        # Extract features from JSON data
        features = np.array([[
            data['lead_time'], 
            data['no_of_special_requests'],
            data['avg_price_per_room'],
            data['arrival_month'], 
            data['arrival_date'],
            data['market_segment_type'],
            data['no_of_week_nights'], 
            data['no_of_weekend_nights'],
            data['type_of_meal_plan'], 
            data['room_type_reserved']
        ]])
        
        # Make prediction
        prediction = loaded_model.predict(features)
        
        result = {
            'prediction': int(prediction[0]),
            'message': 'Likely to confirm booking' if prediction[0] == 1 else 'Likely to cancel booking'
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)