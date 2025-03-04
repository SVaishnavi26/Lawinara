from flask import Flask, render_template, request, jsonify, session, redirect
import pickle
import tensorflow as tf
import numpy as np
from preprocess import extract_features 
from transformers import AutoTokenizer, AutoModel  
from predict1 import predict_case



app = Flask(__name__)
app.secret_key = "Lawinara"


# Load ML models and encoders
try:
    act_model = tf.keras.models.load_model("models/model_act_lstm.keras")
    judg_model = tf.keras.models.load_model("models/model_judg_lstm.keras")
    
    with open("models/label_encoder_act.pkl", "rb") as f:
        act_encoder = pickle.load(f)
    
    with open("models/label_encoder_judgment.pkl", "rb") as f:
        judg_encoder = pickle.load(f)
except Exception as e:
    print(f"Error loading models or encoders: {e}")
    act_model, judg_model, act_encoder, judg_encoder = None, None, None, None

# Routes

@app.route('/')
def landing():
    return render_template('LandingPage.html')

@app.route('/home')
def home():
    return render_template('HomePage.html')

@app.route('/explore')
def explore():
    return render_template('explore.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/model')
def model_page():
    return render_template('model.html')

@app.route('/results')
def results_page():
    act_section = session.get('predicted_act_section', 'No prediction available')
    judgment = session.get('predicted_judgment', 'No prediction available')
    
    return render_template('results.html', act_section=act_section, judgment=judgment)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # For JSON requests from fetch API
        if request.is_json:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            
            # For development - accept any credentials
            session['username'] = username
            return jsonify({
                'success': True,
                'username': username,
                'message': 'Login successful'
            })
        else:
            # For form submissions (if you need this)
            username = request.form.get('username')
            password = request.form.get('password')
            
            session['username'] = username
            return redirect('/home')  # Redirect to home page after login
    
    # If GET request, show login page
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # For JSON requests
        if request.is_json:
            data = request.get_json()
            first_name = data.get('firstName')
            last_name = data.get('lastName')
            email = data.get('email')
            password = data.get('password')
        # For form encoded data
        else:
            first_name = request.form.get('firstName')
            last_name = request.form.get('lastName')
            email = request.form.get('email')
            password = request.form.get('password')
        
        # Here you would typically save the user to a database
        # For now, we'll just store in session like the login route
        session['username'] = f"{first_name} {last_name}"
        session['email'] = email
        
        # Return JSON response for AJAX requests
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': True,
                'message': 'Account created successfully',
                'redirect': '/home'  # Redirect to home page after signup
            })
        # For regular form submissions
        else:
            return redirect('/home')  # Redirect to home page after signup
    
    # If GET request, show signup page
    return render_template('signup.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    case_description = data.get('case_description', '').strip()
    
    if not case_description:
        return jsonify({"error": "Case description is required."}), 400
    
    try:
        prediction = predict_case(case_description)

        # Store predictions in session for results page
        session['predicted_act_section'] = prediction["Predicted Act & Section"]
        session['predicted_judgment'] = prediction["Predicted Judgment"]
        
        return jsonify({
            "act_section": prediction["Predicted Act & Section"],
            "judgment": prediction["Predicted Judgment"],
            "redirect": "/results"
        })
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

@app.route('/get_predictions')
def get_predictions():
    act_section = session.get('predicted_act_section', 'No prediction available')
    judgment = session.get('predicted_judgment', 'No prediction available')
    
    return jsonify({
        'act_section': act_section,
        'judgment': judgment
    })

if __name__ == '__main__':
    app.run(debug=True)