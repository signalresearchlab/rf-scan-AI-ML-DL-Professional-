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
# ml_signal_classifier.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
import xgboost as xgb


class SignalClassifier:
    def __init__(self):
        self.models = {
            'rf': RandomForestClassifier(n_estimators=200),
            'svm': SVC(kernel='rbf', probability=True),
            'xgb': xgb.XGBClassifier(),
            'gb': GradientBoostingClassifier()
        }

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
        spectral_bandwidth = np.sqrt(
            np.sum((np.arange(len(fft)) - spectral_centroid) ** 2 * np.abs(fft)) / np.sum(np.abs(fft)))

        features.extend([
            spectral_centroid,
            spectral_bandwidth,
            np.mean(np.abs(fft)),
            np.std(np.abs(fft))
        ])

        # Advanced signal processing features
        features.extend(self.calculate_modulation_features(iq_data))

        return np.array(features)

    def calculate_modulation_features(self, iq_data):
        # Extract modulation-specific features
        i_data = np.real(iq_data)
        q_data = np.imag(iq_data)

        amplitude = np.sqrt(i_data ** 2 + q_data ** 2)
        phase = np.arctan2(q_data, i_data)
        frequency = np.diff(np.unwrap(phase))

        return [
            np.std(amplitude),  # AM features
            np.std(frequency),  # FM features
            np.std(phase),  # PM features
            np.mean(amplitude),
            np.mean(frequency)
        ]
