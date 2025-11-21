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
# database_setup.py - Initialize SQLite Database
import sqlite3
import os
from datetime import datetime

def setup_database():
    """Create SQLite database with all tables"""
    
    # Create database directory
    os.makedirs('saved_data/database', exist_ok=True)
    
    # Connect to SQLite database (creates if not exists)
    conn = sqlite3.connect('saved_data/database/rf_scanner.db')
    cursor = conn.cursor()
    
    # Table for monitoring sessions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS monitoring_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_start TIMESTAMP,
            session_end TIMESTAMP,
            duration_seconds INTEGER,
            total_scans INTEGER,
            signals_detected INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Table for detected signals
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS detected_signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            timestamp TIMESTAMP,
            frequency_mhz REAL,
            power_dbm REAL,
            signal_type TEXT,
            confidence REAL,
            bandwidth_mhz REAL,
            modulation_type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES monitoring_sessions (id)
        )
    ''')
    
    # Table for spectrum analysis
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS spectrum_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TIMESTAMP,
            center_frequency_mhz REAL,
            bandwidth_mhz REAL,
            peak_power_dbm REAL,
            mean_power_dbm REAL,
            peak_frequency_bin INTEGER,
            total_bands INTEGER,
            noise_floor_dbm REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Table for ML features
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ml_features (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TIMESTAMP,
            feature_vector BLOB,
            feature_count INTEGER,
            signal_class TEXT,
            model_used TEXT,
            confidence REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Table for CNN predictions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cnn_predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TIMESTAMP,
            modulation_type TEXT,
            confidence REAL,
            input_shape TEXT,
            prediction_time_ms REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Table for system logs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TIMESTAMP,
            module_name TEXT,
            log_level TEXT,
            message TEXT,
            data BLOB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    
    print("✅ Database setup completed!")
    print("📁 Database location: saved_data/database/rf_scanner.db")
    
    # Show table info
    show_tables()

def show_tables():
    """Display all tables and their structure"""
    conn = sqlite3.connect('saved_data/database/rf_scanner.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    print("\n📊 Database Tables:")
    for table in tables:
        table_name = table[0]
        print(f"\n{table_name}:")
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        for col in columns:
            print(f"  └── {col[1]} ({col[2]})")
    
    conn.close()

if __name__ == "__main__":
    setup_database()
