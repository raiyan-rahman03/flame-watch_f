import pandas as pd
import numpy as np
import joblib
from tqdm import tqdm
from sklearn.metrics import accuracy_score

# Load the dataset
print("Loading dataset...")
dataset_path = r'C:\Users\Md Raiyan\Desktop\flame\FlameWatch\ml\flame_watch_final_1.csv'
df = pd.read_csv(dataset_path)

# Prepare the original dataset for testing
X = df.drop('is_fire', axis=1)
y = df['is_fire']

# Limit the number of rows (for example, taking the first 100 rows)
n_rows = 100
  # Adjust this number as needed
X = X.head(n_rows)
y = y.head(n_rows)

# Add noise to the dataset
noise_factor = 0.5
df_noisy = X + noise_factor * np.random.randn(*X.shape)

# Convert to DataFrame
df_noisy = pd.DataFrame(df_noisy, columns=X.columns)
df_noisy['is_fire'] = y.values  # Add the target variable back

# List of model filenames to test
model_filenames = [
    r'C:\Users\Md Raiyan\Desktop\flame\FlameWatch\ml\best_rf_model_1.pkl',
    r'C:\Users\Md Raiyan\Desktop\flame\FlameWatch\ml\best_rf_model_2.pkl',
    r'C:\Users\Md Raiyan\Desktop\flame\FlameWatch\ml\best_rf_model_3.pkl',
    r'C:\Users\Md Raiyan\Desktop\flame\FlameWatch\ml\best_rf_model_4.pkl',
    r'C:\Users\Md Raiyan\Desktop\flame\FlameWatch\ml\best_rf_model_f.pkl',
]

# Initialize a dictionary to store accuracies
accuracies = {}

# Test each model
for model_filename in tqdm(model_filenames, desc="Testing models"):
    # Load the trained model
    model = joblib.load(model_filename)

    # Prepare the features and target variable for the noisy dataset
    X_noisy = df_noisy.drop('is_fire', axis=1)  # Features
    y_noisy = df_noisy['is_fire']                # Target

    # Test the model
    y_pred = model.predict(X_noisy)
    accuracy = accuracy_score(y_noisy, y_pred)

    # Store accuracy results
    accuracies[model_filename] = accuracy * 100  # Store accuracy in percentage

# Print the accuracies only
print("Model Accuracies:")
for filename, accuracy in accuracies.items():
    print(f"{filename}: Accuracy: {accuracy:.2f}%")
