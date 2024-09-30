import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score
import joblib
from tqdm import tqdm

# Load the dataset
print("Loading dataset...")
dataset_path = r'C:\Users\Md Raiyan\Desktop\flame\FlameWatch\ml\flame_watch_final_1.csv'
df = pd.read_csv(dataset_path)

# Print the dataset (first 5 rows)
print("Data loaded successfully:")
print(df.head())

# Remove non-numeric columns
print("Removing non-numeric columns...")
df = df.select_dtypes(include=[np.number])

# Fill NaN values with the column mean
print("Filling missing values...")
df = df.fillna(df.mean())

# Separate features (X) and target (y)
print("Separating features and target...")
X = df.drop('is_fire', axis=1)  # Features (all columns except 'is_fire')
y = df['is_fire']               # Target (the 'is_fire' column)

# Split the data into training and testing sets (80% train, 20% test)
print("Splitting data into training and test sets...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Random Forest Classifier with increased n_estimators and parallel processing
print("Initializing Random Forest model...")
model = RandomForestClassifier(n_estimators=400, n_jobs=-1, random_state=42)  # Increased n_estimators

# Perform cross-validation (using 3 folds for faster evaluation)
print("Performing 3-fold cross-validation...")

# Using tqdm to show progress for cross-validation
cv_scores = []
for fold in tqdm(range(3), desc="Cross-validation", unit="fold"):
    score = cross_val_score(model, X_train, y_train, cv=3, n_jobs=-1)  # 3-fold cross-validation
    cv_scores.append(score.mean())

# Average the cross-validation scores
mean_cv_score = np.mean(cv_scores)
print(f"Cross-validation Accuracy: {mean_cv_score * 100:.2f}%")

# Train the model
print("Starting model training...")
model.fit(X_train, y_train)

# Save the trained model
model_filename = r'C:\Users\Md Raiyan\Desktop\flame\FlameWatch\ml\best_rf_model_f.pkl'
print(f"Saving the trained model as {model_filename}...")
joblib.dump(model, model_filename)
print(f"Model saved successfully at {model_filename}!")

# Test the model on the test data
print("Testing the model...")
y_pred = model.predict(X_test)

# Show a progress bar while calculating accuracy
print("Evaluating predictions...")
for _ in tqdm(range(len(y_pred)), desc="Predictions", unit="sample"):
    pass  # Simulating a process for each prediction

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Test Accuracy: {accuracy * 100:.2f}%")
