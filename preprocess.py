import pandas as pd
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel
from tqdm import tqdm  # For progress bar

# Load Dataset
df = pd.read_excel("data/detail.xlsx")  # Ensure the file has a 'Case Description' column

# Load Pre-trained SBERT Model
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

# Function to extract sentence embeddings using SBERT (CLS Token)
def extract_features(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state[:, 0, :].squeeze().numpy()  # CLS token representation

# Apply Feature Extraction (with progress bar)
tqdm.pandas()
df['Features'] = df['Case Description'].progress_apply(lambda x: extract_features(str(x)))

# Convert Feature Column to Numpy Array
X = np.stack(df['Features'].values)
np.save("data/X_features.npy", X)  # Save Features for Model Training

# Save Labels (Acts/Sections and Final Judgment)
df[['Act/Section', 'Final Judgment']].to_csv("data/y_labels.csv", index=False)

print("✅ Preprocessing Complete! Features Saved.")
