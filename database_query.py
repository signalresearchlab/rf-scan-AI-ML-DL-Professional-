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
# database_query.py - Query and Analyze Database Data
import sqlite3
import pandas as pd
from datetime import datetime, timedelta

class DatabaseQuery:
    def __init__(self, db_path='saved_data/database/rf_scanner.db'):
        self.db_path = db_path
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def show_recent_sessions(self, limit=5):
        """Show recent monitoring sessions"""
        conn = self.get_connection()
        df = pd.read_sql_query('''
            SELECT id, session_start, duration_seconds, total_scans, signals_detected
            FROM monitoring_sessions 
            ORDER BY session_start DESC 
            LIMIT ?
        ''', conn, params=(limit,))
        conn.close()
        
        print("📊 Recent Monitoring Sessions:")
        print(df.to_string(index=False))
        return df
    
    def show_recent_signals(self, limit=10):
        """Show recent detected signals"""
        conn = self.get_connection()
        df = pd.read_sql_query('''
            SELECT timestamp, frequency_mhz, power_dbm, signal_type, modulation_type
            FROM detected_signals 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', conn, params=(limit,))
        conn.close()
        
        print("\n📡 Recent Detected Signals:")
        print(df.to_string(index=False))
        return df
    
    def show_signal_statistics(self):
        """Show signal statistics"""
        conn = self.get_connection()
        
        # Total signals by type
        df_type = pd.read_sql_query('''
            SELECT signal_type, COUNT(*) as count, 
                   AVG(power_dbm) as avg_power,
                   AVG(frequency_mhz) as avg_frequency
            FROM detected_signals 
            GROUP BY signal_type
            ORDER BY count DESC
        ''', conn)
        
        # Frequency band statistics
        df_band = pd.read_sql_query('''
            SELECT 
                CASE 
                    WHEN frequency_mhz < 1000 THEN 'VHF/UHF'
                    WHEN frequency_mhz BETWEEN 1000 AND 3000 THEN 'L-Band' 
                    ELSE 'S-Band+'
                END as frequency_band,
                COUNT(*) as signal_count,
                AVG(power_dbm) as avg_power
            FROM detected_signals 
            GROUP BY frequency_band
            ORDER BY signal_count DESC
        ''', conn)
        
        conn.close()
        
        print("\n📈 Signal Statistics by Type:")
        print(df_type.to_string(index=False))
        
        print("\n📊 Signal Statistics by Frequency Band:")
        print(df_band.to_string(index=False))
        
        return df_type, df_band
    
    def show_database_info(self):
        """Show database information"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        tables = ['monitoring_sessions', 'detected_signals', 'spectrum_analysis', 
                 'ml_features', 'cnn_predictions', 'system_logs']
        
        print("🗃️ Database Information:")
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"  {table:20} : {count:4} records")
        
        conn.close()
    
    def export_to_csv(self, table_name, output_file):
        """Export table to CSV"""
        conn = self.get_connection()
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        df.to_csv(output_file, index=False)
        conn.close()
        print(f"💾 Exported {table_name} to {output_file}")

def main():
    """Main function for database queries"""
    query = DatabaseQuery()
    
    print("🔍 RF Scanner Database Query Tool")
    print("=" * 50)
    
    while True:
        print("\nAvailable Queries:")
        print("1. Show recent sessions")
        print("2. Show recent signals") 
        print("3. Show signal statistics")
        print("4. Show database info")
        print("5. Export signals to CSV")
        print("6. Exit")
        
        choice = input("\nSelect option (1-6): ").strip()
        
        if choice == '1':
            query.show_recent_sessions()
        elif choice == '2':
            query.show_recent_signals()
        elif choice == '3':
            query.show_signal_statistics()
        elif choice == '4':
            query.show_database_info()
        elif choice == '5':
            query.export_to_csv('detected_signals', 'saved_data/exported_signals.csv')
        elif choice == '6':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()
