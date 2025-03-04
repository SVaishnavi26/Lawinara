import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib

# Load Processed Data
X = np.load("data/X_features.npy")
y = pd.read_csv("data/y_labels.csv")

# Encode Labels
le_act = LabelEncoder()
y_act = le_act.fit_transform(y['Act/Section'])

le_judgment = LabelEncoder()
y_judgment = le_judgment.fit_transform(y['Final Judgment'])

# Convert Labels to Categorical
y_act = tf.keras.utils.to_categorical(y_act)
y_judgment = tf.keras.utils.to_categorical(y_judgment)

# Split Data
X_train, X_test, y_train_act, y_test_act = train_test_split(X, y_act, test_size=0.2, random_state=42)
X_train_judg, X_test_judg, y_train_judg, y_test_judg = train_test_split(X, y_judgment, test_size=0.2, random_state=42)

# Reshape Data for LSTM (LSTM expects 3D input: [samples, timesteps, features])
X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

X_train_judg = X_train_judg.reshape(X_train_judg.shape[0], X_train_judg.shape[1], 1)
X_test_judg = X_test_judg.reshape(X_test_judg.shape[0], X_test_judg.shape[1], 1)

# Define LSTM Model
def build_lstm_model(output_dim, input_shape):
    model = Sequential([
        LSTM(256, return_sequences=True, input_shape=input_shape),
        Dropout(0.3),
        LSTM(128, return_sequences=True),
        Dropout(0.3),
        LSTM(64, return_sequences=False),
        Dropout(0.3),
        Dense(128, activation='relu'),
        Dense(output_dim, activation='softmax')
    ])
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

# Train Act/Section Prediction Model
model_act = build_lstm_model(y_train_act.shape[1], (X_train.shape[1], 1))
model_act.fit(X_train, y_train_act, epochs=10, batch_size=32, validation_data=(X_test, y_test_act))
model_act.save("models/model_act_lstm.keras")

# Train Final Judgment Prediction Model
model_judg = build_lstm_model(y_train_judg.shape[1], (X_train_judg.shape[1], 1))
model_judg.fit(X_train_judg, y_train_judg, epochs=10, batch_size=32, validation_data=(X_test_judg, y_test_judg))
model_judg.save("models/model_judg_lstm.keras")

# Save Label Encoders
joblib.dump(le_act, "models/label_encoder_act.pkl")
joblib.dump(le_judgment, "models/label_encoder_judgment.pkl")

print("✅ LSTM Model training completed and saved successfully!")
