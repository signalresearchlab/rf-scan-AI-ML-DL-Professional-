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
# dashboard.py - Real-time RF Monitoring Dashboard
import sqlite3
import pandas as pd
import time
from datetime import datetime, timedelta

class RFDashboard:
    def __init__(self):
        self.db_path = 'saved_data/database/rf_scanner.db'
    
    def get_realtime_stats(self):
        """Get real-time statistics"""
        conn = sqlite3.connect(self.db_path)
        
        stats = {
            'total_signals': pd.read_sql('SELECT COUNT(*) as count FROM detected_signals', conn).iloc[0]['count'],
            'today_signals': pd.read_sql('''SELECT COUNT(*) as count FROM detected_signals 
                                          WHERE date(timestamp) = date('now')''', conn).iloc[0]['count'],
            'signal_types': pd.read_sql('''SELECT signal_type, COUNT(*) as count 
                                         FROM detected_signals GROUP BY signal_type''', conn),
            'recent_activity': pd.read_sql('''SELECT * FROM detected_signals 
                                           ORDER BY timestamp DESC LIMIT 5''', conn),
            'frequency_bands': pd.read_sql('''SELECT 
                CASE 
                    WHEN frequency_mhz < 300 THEN 'VHF'
                    WHEN frequency_mhz BETWEEN 300 AND 1000 THEN 'UHF'
                    WHEN frequency_mhz BETWEEN 1000 AND 3000 THEN 'L-Band'
                    ELSE 'S-Band+'
                END as band,
                COUNT(*) as count
                FROM detected_signals 
                GROUP BY band''', conn)
        }
        
        conn.close()
        return stats
    
    def show_dashboard(self):
        """Display real-time dashboard"""
        while True:
            stats = self.get_realtime_stats()
            
            print("\n" + "="*60)
            print("           🛰️  REAL-TIME RF MONITORING DASHBOARD")
            print("="*60)
            print(f"📊 Total Signals: {stats['total_signals']} | Today: {stats['today_signals']}")
            print(f"🕒 Last Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            print("\n📡 Signal Types Distribution:")
            for _, row in stats['signal_types'].iterrows():
                print(f"   {row['signal_type']:12} : {row['count']:3} signals")
            
            print("\n📶 Frequency Band Usage:")
            for _, row in stats['frequency_bands'].iterrows():
                print(f"   {row['band']:8} : {row['count']:3} signals")
            
            print("\n🔍 Recent Signals:")
            for _, row in stats['recent_activity'].iterrows():
                print(f"   {row['timestamp'][11:19]} - {row['frequency_mhz']:8.1f} MHz - {row['power_dbm']:6.1f} dBm - {row['signal_type']}")
            
            print("\n" + "="*60)
            print("Press Ctrl+C to exit | Auto-refresh every 10 seconds")
            print("="*60)
            
            time.sleep(10)

if __name__ == "__main__":
    dashboard = RFDashboard()
    try:
        dashboard.show_dashboard()
    except KeyboardInterrupt:
        print("\n👋 Dashboard closed")
