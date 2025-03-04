from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf
import pickle
from preprocess import preprocess_text  # Assuming preprocess_text is defined in preprocess.py

app = Flask(__name__)

# Load models
model_act = tf.keras.models.load_model("models/model_act_lstm.keras")
model_judgment = tf.keras.models.load_model("models/model_judg_lstm.keras")

# Load label encoders
with open("models/label_encoder_act.pkl", "rb") as f:
    label_encoder_act = pickle.load(f)

with open("models/label_encoder_judgment.pkl", "rb") as f:
    label_encoder_judgment = pickle.load(f)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        case_description = data.get("case_description", "")

        if not case_description:
            return jsonify({"error": "No case description provided"}), 400

        # Preprocess input
        processed_text = preprocess_text(case_description)  # Modify this function as needed
        input_features = np.array([processed_text])  # Convert to model input format

        # Predict act/section
        act_pred = model_act.predict(input_features)
        act_label = label_encoder_act.inverse_transform([np.argmax(act_pred)])

        # Predict judgment
        judgment_pred = model_judgment.predict(input_features)
        judgment_label = label_encoder_judgment.inverse_transform([np.argmax(judgment_pred)])

        return jsonify({
            "predicted_act": act_label[0],
            "predicted_judgment": judgment_label[0]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
