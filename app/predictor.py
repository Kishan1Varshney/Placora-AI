# ============================================
# PLACORA - Module 3
# Placement Prediction ML Model
# File: app/predictor.py
# ============================================

import pandas as pd
import numpy as np
import os
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report

def generate_sample_dataset(n_samples=500):
    np.random.seed(42)
    data = {
        'cgpa': np.round(np.random.uniform(5.0, 10.0, n_samples), 1),
        'skills_count': np.random.randint(2, 20, n_samples),
        'projects_count': np.random.randint(0, 8, n_samples),
        'certifications_count': np.random.randint(0, 6, n_samples),
        'internship': np.random.randint(0, 2, n_samples),
        'communication': np.random.randint(1, 6, n_samples),
        'backlogs': np.random.randint(0, 5, n_samples),
        'ats_score': np.random.randint(30, 100, n_samples),
    }
    df = pd.DataFrame(data)
    placement_score = (
        (df['cgpa'] - 5) * 0.25 +
        df['skills_count'] * 0.15 +
        df['projects_count'] * 0.2 +
        df['certifications_count'] * 0.1 +
        df['internship'] * 1.5 +
        df['communication'] * 0.2 +
        df['ats_score'] * 0.02 -
        df['backlogs'] * 0.3
    )
    placement_score = (placement_score - placement_score.min()) / (placement_score.max() - placement_score.min())
    noise = np.random.uniform(-0.1, 0.1, n_samples)
    placement_score = np.clip(placement_score + noise, 0, 1)
    df['placed'] = (placement_score > 0.5).astype(int)
    return df


def train_placement_model(save_model=True):
    print("Dataset generate kar rahe hain...")
    df = generate_sample_dataset(500)
    feature_cols = [
        'cgpa', 'skills_count', 'projects_count',
        'certifications_count', 'internship',
        'communication', 'backlogs', 'ats_score'
    ]
    X = df[feature_cols]
    y = df['placed']
    print(f"Dataset ready: {len(df)} samples")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled  = scaler.transform(X_test)
    print("Random Forest model train kar rahe hain...")
    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    report   = classification_report(y_test, y_pred, target_names=['Not Placed', 'Placed'])
    print(f"Model Accuracy: {accuracy*100:.1f}%")
    if save_model:
        os.makedirs('models', exist_ok=True)
        joblib.dump(model,  'models/placement_model.pkl')
        joblib.dump(scaler, 'models/scaler.pkl')
        print("Model saved!")
    return model, scaler, accuracy, report


def predict_placement(cgpa, skills_count, projects_count,
                       certifications_count, internship,
                       communication, backlogs, ats_score,
                       model=None, scaler=None):
    if model is None or scaler is None:
        try:
            model  = joblib.load('models/placement_model.pkl')
            scaler = joblib.load('models/scaler.pkl')
        except FileNotFoundError:
            print("Model nahi mila! Pehle train_placement_model() run karo.")
            return None, None, None
    features = np.array([[
        cgpa, skills_count, projects_count,
        certifications_count, internship,
        communication, backlogs, ats_score
    ]])
    features_scaled = scaler.transform(features)
    probability = model.predict_proba(features_scaled)[0][1] * 100
    prediction  = "Placed" if probability >= 50 else "Not Placed"
    if probability >= 80:
        confidence = "High"
    elif probability >= 60:
        confidence = "Medium"
    elif probability >= 40:
        confidence = "Low"
    else:
        confidence = "Very Low"
    return round(probability, 1), prediction, confidence


def get_improvement_suggestions(cgpa, skills_count, projects_count,
                                  certifications_count, internship,
                                  communication, backlogs, ats_score,
                                  probability):
    suggestions = []
    if probability < 50:
        priority = "Urgent improvement needed!"
    elif probability < 70:
        priority = "Good progress, thoda aur karo!"
    else:
        priority = "Excellent profile! Keep it up!"

    if cgpa < 7.0:
        suggestions.append({'area': 'CGPA', 'fix': f'CGPA {cgpa} kam hai. 7.5+ target rakho.'})
    if skills_count < 8:
        suggestions.append({'area': 'Skills', 'fix': f'Sirf {skills_count} skills hain. Python, SQL, ML seekho. 10+ target.'})
    if projects_count < 3:
        suggestions.append({'area': 'Projects', 'fix': f'Sirf {projects_count} projects. GitHub pe 3-4 real projects daalo.'})
    if certifications_count < 2:
        suggestions.append({'area': 'Certifications', 'fix': 'Google/Coursera se 2-3 certifications lo.'})
    if internship == 0:
        suggestions.append({'area': 'Internship', 'fix': 'Internshala ya LinkedIn pe apply karo.'})
    if communication < 3:
        suggestions.append({'area': 'Communication', 'fix': 'Mock interviews practice karo. GD sessions join karo.'})
    if backlogs > 0:
        suggestions.append({'area': 'Backlogs', 'fix': f'{backlogs} backlogs hain. Pehle inhe clear karo.'})
    if ats_score < 60:
        suggestions.append({'area': 'Resume/ATS', 'fix': f'ATS Score {ats_score}/100. Resume mein keywords add karo.'})

    return priority, suggestions


if __name__ == "__main__":
    print("=" * 50)
    print("   PLACORA - Placement Prediction Model")
    print("=" * 50)
    model, scaler, accuracy, report = train_placement_model(save_model=True)

    print("\nStudent Test:")
    students = [
        ("Rahul - Strong", 8.5, 12, 4, 3, 1, 4, 0, 82),
        ("Priya - Average", 6.8, 6, 2, 1, 0, 3, 1, 55),
        ("Amit - Weak",    5.5, 3, 1, 0, 0, 2, 3, 35),
    ]
    for s in students:
        name = s[0]
        args = s[1:]
        prob, pred, conf = predict_placement(*args, model=model, scaler=scaler)
        print(f"\n  {name}")
        print(f"  Placement Probability: {prob}%  |  {pred}  |  Confidence: {conf}")
