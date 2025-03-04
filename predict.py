import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel
import tensorflow as tf
import joblib  # Changed from pickle to joblib
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"  # Hide TensorFlow info & warnings 

# Load Pre-trained SBERT Model
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

# Load Pre-trained LSTM Models
model_act = tf.keras.models.load_model("models/model_act_lstm.keras")
model_judg = tf.keras.models.load_model("models/model_judg_lstm.keras")

# Load Label Encoders using joblib instead of pickle
label_encoder_act = joblib.load("models/label_encoder_act.pkl")
label_encoder_judg = joblib.load("models/label_encoder_judgment.pkl")

# Function to extract sentence embeddings using SBERT
def extract_features(text):
    try:
        if not text or not isinstance(text, str):  # Handle empty input
            return np.zeros(384)  # Ensure consistent input shape
        
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding="max_length", max_length=512)
        with torch.no_grad():
            outputs = model(**inputs)
        return outputs.last_hidden_state[:, 0, :].squeeze().numpy()  # CLS token representation
        
    except Exception as e:
        print(f"Error extracting features: {e}")
        return np.zeros(384)  # Return a zero vector if extraction fails

# Function to make predictions
def predict_case(case_description):
    try:
        # Extract features
        features = extract_features(case_description)
        features = np.expand_dims(features, axis=0)  # Reshape for model input
        
        # Add debugging to check shapes
        features = features.reshape(features.shape[0], features.shape[1], 1)  # Reshape for LSTM input
        
        # Predict Act/Section
        act_probs = model_act.predict(features)
        act_pred = np.argmax(act_probs, axis=1)
        
        if act_pred.size == 0:
            return {"error": "Act prediction failed"}
        
        # Debug types before inverse_transform
        print(f"label_encoder_act type: {type(label_encoder_act)}")
        print(f"act_pred type: {type(act_pred)}, value: {act_pred}")
        
        act_label = label_encoder_act.inverse_transform(act_pred)[0]
        
        # Predict Final Judgment
        judg_probs = model_judg.predict(features)
        judg_pred = np.argmax(judg_probs, axis=1)
        
        if judg_pred.size == 0:
            return {"error": "Judgment prediction failed"}
        
        judg_label = label_encoder_judg.inverse_transform(judg_pred)[0]
        
        return {
            "Predicted Act/Section": act_label,
            "Predicted Judgment": judg_label
        }
        
    except Exception as e:
        return {"error": f"Prediction error: {str(e)}"}
