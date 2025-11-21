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
# database_manager.py - SQL Database Manager
import sqlite3
import json
import numpy as np
from datetime import datetime
import time

class DatabaseManager:
    def __init__(self, db_path='saved_data/database/rf_scanner.db'):
        self.db_path = db_path
        self.current_session_id = None
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def start_monitoring_session(self, duration_seconds):
        """Start a new monitoring session"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO monitoring_sessions 
            (session_start, duration_seconds, total_scans, signals_detected)
            VALUES (?, ?, 0, 0)
        ''', (datetime.now(), duration_seconds))
        
        self.current_session_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        print(f"📊 Database: Started monitoring session #{self.current_session_id}")
        return self.current_session_id
    
    def save_detected_signal(self, frequency, power, signal_type='unknown', confidence=0.0, bandwidth=0.0, modulation=None):
        """Save detected signal to database"""
        if not self.current_session_id:
            print("❌ No active monitoring session")
            return
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO detected_signals 
            (session_id, timestamp, frequency_mhz, power_dbm, signal_type, confidence, bandwidth_mhz, modulation_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            self.current_session_id,
            datetime.now(),
            frequency/1e6,  # Convert to MHz
            power,
            signal_type,
            confidence,
            bandwidth,
            modulation
        ))
        
        # Update session statistics
        cursor.execute('''
            UPDATE monitoring_sessions 
            SET signals_detected = signals_detected + 1 
            WHERE id = ?
        ''', (self.current_session_id,))
        
        conn.commit()
        conn.close()
        
        print(f"💾 Database: Saved signal at {frequency/1e6:.1f} MHz")
    
    def save_spectrum_analysis(self, center_freq, bandwidth, peak_power, mean_power, peak_freq_bin, total_bands, noise_floor=-90.0):
        """Save spectrum analysis results"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO spectrum_analysis 
            (timestamp, center_frequency_mhz, bandwidth_mhz, peak_power_dbm, mean_power_dbm, 
             peak_frequency_bin, total_bands, noise_floor_dbm)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now(),
            center_freq/1e6,  # Convert to MHz
            bandwidth/1e6,    # Convert to MHz
            peak_power,
            mean_power,
            peak_freq_bin,
            total_bands,
            noise_floor
        ))
        
        conn.commit()
        conn.close()
        
        print(f"💾 Database: Saved spectrum analysis")
    
    def save_ml_features(self, features, signal_class='unknown', model_used='rf', confidence=0.0):
        """Save ML features to database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Convert numpy array to JSON string
        features_json = json.dumps(features.tolist() if isinstance(features, np.ndarray) else features)
        
        cursor.execute('''
            INSERT INTO ml_features 
            (timestamp, feature_vector, feature_count, signal_class, model_used, confidence)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now(),
            features_json,
            len(features),
            signal_class,
            model_used,
            confidence
        ))
        
        conn.commit()
        conn.close()
        
        print(f"💾 Database: Saved {len(features)} ML features")
    
    def save_cnn_prediction(self, modulation_type, confidence, input_shape, prediction_time_ms=0.0):
        """Save CNN prediction results"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO cnn_predictions 
            (timestamp, modulation_type, confidence, input_shape, prediction_time_ms)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            datetime.now(),
            modulation_type,
            confidence,
            str(input_shape),
            prediction_time_ms
        ))
        
        conn.commit()
        conn.close()
        
        print(f"💾 Database: Saved CNN prediction: {modulation_type} ({confidence:.2%})")
    
    def save_system_log(self, module_name, message, log_level='INFO', data=None):
        """Save system logs to database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        data_json = json.dumps(data) if data else None
        
        cursor.execute('''
            INSERT INTO system_logs 
            (timestamp, module_name, log_level, message, data)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            datetime.now(),
            module_name,
            log_level,
            message,
            data_json
        ))
        
        conn.commit()
        conn.close()
    
    def end_monitoring_session(self, total_scans=0):
        """End the current monitoring session"""
        if not self.current_session_id:
            return
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE monitoring_sessions 
            SET session_end = ?, total_scans = ?
            WHERE id = ?
        ''', (datetime.now(), total_scans, self.current_session_id))
        
        conn.commit()
        conn.close()
        
        print(f"📊 Database: Ended monitoring session #{self.current_session_id}")
        self.current_session_id = None
    
    def get_recent_signals(self, limit=10):
        """Get recent detected signals"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT timestamp, frequency_mhz, power_dbm, signal_type, modulation_type
            FROM detected_signals 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
        
        signals = cursor.fetchall()
        conn.close()
        return signals
    
    def get_session_statistics(self, session_id=None):
        """Get statistics for a session"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if session_id:
            cursor.execute('''
                SELECT * FROM monitoring_sessions WHERE id = ?
            ''', (session_id,))
        else:
            cursor.execute('''
                SELECT * FROM monitoring_sessions 
                ORDER BY session_start DESC 
                LIMIT 1
            ''')
        
        session = cursor.fetchone()
        conn.close()
        return session

# Test the database manager
if __name__ == "__main__":
    db = DatabaseManager()
    print("✅ Database Manager initialized")
    
    # Test functionality
    session_id = db.start_monitoring_session(60)
    db.save_detected_signal(2.4e9, -45.5, 'WIFI', 0.85, 20.0, 'OFDM')
    db.save_spectrum_analysis(100e6, 10e6, -30.5, -65.2, 128, 1024)
    db.save_ml_features([1.2, 3.4, 5.6, 7.8], 'WIFI', 'rf', 0.92)
    db.save_cnn_prediction('QPSK', 0.78, (1024, 2), 15.5)
    db.save_system_log('database_test', 'Test log entry')
    
    # Show recent signals
    recent = db.get_recent_signals(5)
    print("\n📡 Recent signals from database:")
    for signal in recent:
        print(f"  {signal[0]}: {signal[1]} MHz, {signal[2]} dBm, {signal[3]}")
    
    db.end_monitoring_session(10)
