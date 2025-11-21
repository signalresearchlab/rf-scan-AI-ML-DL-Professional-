#!/usr/bin/env python3
"""
RF Scanner AI - Educational Use Only
====================================
WARNING: This software is for EDUCATIONAL and RESEARCH purposes only.

PROHIBITED: Illegal surveillance, privacy violation, unauthorized access
LEGAL: Users must comply with all applicable laws and regulations

Developer: Shahnawaz Khurram - Signal Research Lab
Contact: signalresearchlab@gmail.com
"""
# ml.py - Machine Learning Signal Classifier with Data Saving
import pandas as pd
import numpy as np
import json
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
import xgboost as xgb
from datetime import datetime

class SignalClassifier:
    def __init__(self):
        self.models = {
            'rf': RandomForestClassifier(n_estimators=200),
            'svm': SVC(kernel='rbf', probability=True),
            'xgb': xgb.XGBClassifier(),
            'gb': GradientBoostingClassifier()
        }
        self.feature_data = []
        self.setup_ml_files()

    def setup_ml_files(self):
        """Setup files for ML data"""
        os.makedirs('saved_data/ml', exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.features_file = f"saved_data/ml/features_{timestamp}.csv"
        self.models_file = f"saved_data/ml/models_info_{timestamp}.json"
        
        print(f"📁 ML data will be saved to:")
        print(f"   Features CSV: {self.features_file}")
        print(f"   Models info:  {self.models_file}")

    def save_features(self, iq_data, features):
        """Save extracted features"""
        timestamp = datetime.now().isoformat()
        
        feature_row = [timestamp] + features.tolist()
        with open(self.features_file, 'a') as f:
            f.write(','.join(map(str, feature_row)) + '\n')
        
        print(f"💾 Saved {len(features)} features from IQ data")

    def save_models_info(self):
        """Save information about trained models"""
        models_info = {
            'timestamp': datetime.now().isoformat(),
            'models': list(self.models.keys()),
            'feature_count': len(self.feature_data),
            'model_types': {name: type(model).__name__ for name, model in self.models.items()}
        }
        
        with open(self.models_file, 'w') as f:
            json.dump(models_info, f, indent=2)
        
        print(f"📁 ML models info saved to: {self.models_file}")

    def extract_advanced_features(self, iq_data):
        features = []
        
        # Time domain features
        features.extend([
            np.mean(np.abs(iq_data)),
            np.std(iq_data),
            np.var(iq_data),
            np.max(np.abs(iq_data)),
            np.min(np.abs(iq_data))
        ])
        
        # Frequency domain features
        fft = np.fft.fft(iq_data)
        spectral_centroid = np.sum(np.arange(len(fft)) * np.abs(fft)) / np.sum(np.abs(fft))
        spectral_bandwidth = np.sqrt(np.sum((np.arange(len(fft)) - spectral_centroid)**2 * np.abs(fft)) / np.sum(np.abs(fft)))
        
        features.extend([
            spectral_centroid,
            spectral_bandwidth,
            np.mean(np.abs(fft)),
            np.std(np.abs(fft))
        ])
        
        return np.array(features)

def main():
    """Main function for ML analysis"""
    print("Starting Machine Learning Signal Classifier...")
    
    try:
        classifier = SignalClassifier()
        print("✅ ML Classifier initialized!")
        print(f"🤖 Available models: {list(classifier.models.keys())}")
        
        # Simulate feature extraction
        print("\n🔬 Simulating feature extraction...")
        test_iq = np.random.randn(1024) + 1j * np.random.randn(1024)
        features = classifier.extract_advanced_features(test_iq)
        
        # Save the features
        classifier.save_features(test_iq, features)
        classifier.save_models_info()
        
        print(f"📊 Extracted {len(features)} features from IQ data")
        print(f"📐 Feature vector: {features[:5]}...")
        
    except Exception as e:
        print(f"❌ ML analysis error: {e}")

if __name__ == "__main__":
    main()
