"""
Train all 6 ML classification models on the lung cancer survey dataset.
Models: Logistic Regression, Decision Tree, Random Forest, SVM, KNN, Naive Bayes
"""
import os
import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import joblib

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'survey lung cancer.csv')
MODELS_DIR = os.path.join(BASE_DIR, 'ml_models')

def load_and_preprocess_data():
    """Load the dataset and preprocess it."""
    print("=" * 60)
    print("LUNG CANCER PREDICTION - MODEL TRAINING")
    print("=" * 60)
    
    # Load dataset
    df = pd.read_csv(DATA_PATH)
    print(f"\nDataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"Columns: {list(df.columns)}")
    
    # Clean column names (strip whitespace)
    df.columns = df.columns.str.strip()
    
    # Encode GENDER: M=1, F=0
    df['GENDER'] = df['GENDER'].map({'M': 1, 'F': 0})
    
    # Encode target: YES=1, NO=0
    df['LUNG_CANCER'] = df['LUNG_CANCER'].map({'YES': 1, 'NO': 0})
    
    # Check for any missing values
    if df.isnull().sum().sum() > 0:
        print(f"\nMissing values found: {df.isnull().sum().sum()}")
        df = df.dropna()
        print(f"After dropping NaN: {df.shape[0]} rows")
    else:
        print("\nNo missing values found.")
    
    # Separate features and target
    X = df.drop('LUNG_CANCER', axis=1)
    y = df['LUNG_CANCER']
    
    print(f"\nTarget distribution:")
    print(f"  YES (1): {(y == 1).sum()} ({(y == 1).mean()*100:.1f}%)")
    print(f"  NO  (0): {(y == 0).sum()} ({(y == 0).mean()*100:.1f}%)")
    
    return X, y

def train_and_evaluate_models(X, y):
    """Train all 6 models and evaluate them."""
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\nTraining set: {X_train.shape[0]} samples")
    print(f"Testing set:  {X_test.shape[0]} samples")
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Save scaler
    joblib.dump(scaler, os.path.join(MODELS_DIR, 'scaler.pkl'))
    print("\nScaler saved.")
    
    # Define models
    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        'Decision Tree': DecisionTreeClassifier(random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'SVM': SVC(kernel='rbf', probability=True, random_state=42),
        'KNN': KNeighborsClassifier(n_neighbors=5),
        'Naive Bayes': GaussianNB()
    }
    
    results = {}
    
    print("\n" + "=" * 60)
    print("TRAINING & EVALUATING MODELS")
    print("=" * 60)
    
    for name, model in models.items():
        print(f"\n--- {name} ---")
        
        # Train
        model.fit(X_train_scaled, y_train)
        
        # Predict
        y_pred = model.predict(X_test_scaled)
        
        # Metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, zero_division=0)
        recall = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        cm = confusion_matrix(y_test, y_pred).tolist()
        
        print(f"  Accuracy:  {accuracy*100:.2f}%")
        print(f"  Precision: {precision*100:.2f}%")
        print(f"  Recall:    {recall*100:.2f}%")
        print(f"  F1-Score:  {f1*100:.2f}%")
        print(f"  Confusion Matrix: {cm}")
        
        # Save model
        model_filename = name.lower().replace(' ', '_') + '.pkl'
        joblib.dump(model, os.path.join(MODELS_DIR, model_filename))
        print(f"  Model saved: {model_filename}")
        
        results[name] = {
            'accuracy': round(accuracy * 100, 2),
            'precision': round(precision * 100, 2),
            'recall': round(recall * 100, 2),
            'f1_score': round(f1 * 100, 2),
            'confusion_matrix': cm,
            'model_file': model_filename
        }
    
    # Save feature names
    feature_names = list(X.columns)
    joblib.dump(feature_names, os.path.join(MODELS_DIR, 'feature_names.pkl'))
    
    # Find best model
    best_model = max(results, key=lambda k: results[k]['accuracy'])
    results['best_model'] = best_model
    
    # Save results
    with open(os.path.join(MODELS_DIR, 'model_results.json'), 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"\nBest Model: {best_model} ({results[best_model]['accuracy']}%)")
    print(f"\nAll results saved to ml_models/model_results.json")
    print("All models saved to ml_models/")
    
    return results

if __name__ == '__main__':
    # Create models directory
    os.makedirs(MODELS_DIR, exist_ok=True)
    
    # Load and preprocess
    X, y = load_and_preprocess_data()
    
    # Train and evaluate
    results = train_and_evaluate_models(X, y)
    
    print("\n[OK] Training complete!")
