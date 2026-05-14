"""
ML Models loader and prediction module for lung cancer prediction.
Loads trained models and provides prediction functionality.
"""
import os
import json
import numpy as np
import joblib
from django.conf import settings

MODELS_DIR = settings.ML_MODELS_DIR

# Model names and their file names
MODEL_INFO = {
    'Logistic Regression': 'logistic_regression.pkl',
    'Decision Tree': 'decision_tree.pkl',
    'Random Forest': 'random_forest.pkl',
    'SVM': 'svm.pkl',
    'KNN': 'knn.pkl',
    'Naive Bayes': 'naive_bayes.pkl',
}

def load_models():
    """Load all trained ML models."""
    models = {}
    for name, filename in MODEL_INFO.items():
        model_path = os.path.join(MODELS_DIR, filename)
        if os.path.exists(model_path):
            models[name] = joblib.load(model_path)
    return models

def load_scaler():
    """Load the trained StandardScaler."""
    scaler_path = os.path.join(MODELS_DIR, 'scaler.pkl')
    if os.path.exists(scaler_path):
        return joblib.load(scaler_path)
    return None

def load_results():
    """Load model evaluation results."""
    results_path = os.path.join(MODELS_DIR, 'model_results.json')
    if os.path.exists(results_path):
        with open(results_path, 'r') as f:
            return json.load(f)
    return None

def predict(input_data):
    """
    Run prediction through all 6 models.
    
    Args:
        input_data: dict with keys matching feature names
            {
                'GENDER': 'M' or 'F',
                'AGE': int,
                'SMOKING': 1 or 2,
                'YELLOW_FINGERS': 1 or 2,
                ... etc
            }
    
    Returns:
        dict with predictions from each model and accuracy info
    """
    models = load_models()
    scaler = load_scaler()
    results_data = load_results()
    
    if not models or scaler is None:
        return None
    
    # Prepare input features
    gender = 1 if input_data.get('GENDER') == 'M' else 0
    
    features = np.array([[
        gender,
        int(input_data.get('AGE', 50)),
        int(input_data.get('SMOKING', 1)),
        int(input_data.get('YELLOW_FINGERS', 1)),
        int(input_data.get('ANXIETY', 1)),
        int(input_data.get('PEER_PRESSURE', 1)),
        int(input_data.get('CHRONIC_DISEASE', 1)),
        int(input_data.get('FATIGUE', 1)),
        int(input_data.get('ALLERGY', 1)),
        int(input_data.get('WHEEZING', 1)),
        int(input_data.get('ALCOHOL_CONSUMING', 1)),
        int(input_data.get('COUGHING', 1)),
        int(input_data.get('SHORTNESS_OF_BREATH', 1)),
        int(input_data.get('SWALLOWING_DIFFICULTY', 1)),
        int(input_data.get('CHEST_PAIN', 1)),
    ]])
    
    # Scale features
    features_scaled = scaler.transform(features)
    
    # Get predictions from all models
    predictions = {}
    yes_count = 0
    total = 0
    
    for name, model in models.items():
        pred = model.predict(features_scaled)[0]
        pred_label = 'YES' if pred == 1 else 'NO'
        
        # Get probability if available
        prob = None
        if hasattr(model, 'predict_proba'):
            prob = model.predict_proba(features_scaled)[0]
            prob = round(float(max(prob)) * 100, 2)
        
        accuracy = results_data.get(name, {}).get('accuracy', 'N/A') if results_data else 'N/A'
        
        predictions[name] = {
            'prediction': pred_label,
            'confidence': prob,
            'accuracy': accuracy,
        }
        
        if pred == 1:
            yes_count += 1
        total += 1
    
    # Overall result based on majority voting
    overall = 'YES' if yes_count > total / 2 else 'NO'
    
    # Best model
    best_model = results_data.get('best_model', 'Random Forest') if results_data else 'Random Forest'
    
    return {
        'predictions': predictions,
        'overall_result': overall,
        'best_model': best_model,
        'yes_count': yes_count,
        'total_models': total,
    }
