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
# enhanced_dashboard.py - Dashboard with Alerts and Analytics
import sqlite3
import pandas as pd
import time
import os
from datetime import datetime, timedelta
from alerts import RFAlertSystem

class EnhancedRFDashboard:
    def __init__(self):
        self.db_path = 'saved_data/database/rf_scanner.db'
        self.alert_system = RFAlertSystem()
    
    def get_system_health(self):
        """Get system health metrics"""
        conn = sqlite3.connect(self.db_path)
        
        health = {
            'database_size': os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0,
            'uptime_hours': 1,  # Simplified - would track actual uptime
            'error_rate': 0,    # Simplified - would track actual errors
            'storage_used': self.get_storage_usage()
        }
        
        conn.close()
        return health
    
    def get_storage_usage(self):
        """Calculate storage usage"""
        total_size = 0
        if os.path.exists('saved_data'):
            for dirpath, dirnames, filenames in os.walk('saved_data'):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    total_size += os.path.getsize(fp)
        return total_size / (1024 * 1024)  # Convert to MB
    
    def get_signal_trends(self):
        """Get signal trends over time"""
        conn = sqlite3.connect(self.db_path)
        
        # Last hour trends
        df = pd.read_sql('''
            SELECT 
                strftime('%Y-%m-%d %H:%M:00', timestamp) as minute,
                COUNT(*) as signal_count,
                AVG(power_dbm) as avg_power
            FROM detected_signals 
            WHERE timestamp > datetime('now', '-1 hour')
            GROUP BY minute
            ORDER BY minute
        ''', conn)
        
        conn.close()
        return df
    
    def show_enhanced_dashboard(self):
        """Display enhanced dashboard with alerts and analytics"""
        while True:
            # Clear screen (works on most terminals)
            os.system('clear' if os.name == 'posix' else 'cls')
            
            stats = self.get_realtime_stats()
            health = self.get_system_health()
            alerts = self.alert_system.check_alerts()
            trends = self.get_signal_trends()
            
            print("\n" + "="*70)
            print("           🛰️  ENHANCED RF MONITORING DASHBOARD")
            print("="*70)
            print(f"📊 Total Signals: {stats['total_signals']:4} | Today: {stats['today_signals']:3} | Storage: {health['storage_used']:.1f} MB")
            print(f"🕒 Last Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Uptime: {health['uptime_hours']}h")
            
            # Alert Section
            if alerts:
                print(f"\n🚨 ACTIVE ALERTS ({len(alerts)}):")
                for alert in alerts[:3]:  # Show max 3 alerts
                    print(f"   ⚠️  {alert['severity']}: {alert['message']}")
                if len(alerts) > 3:
                    print(f"   ... and {len(alerts) - 3} more alerts")
            else:
                print(f"\n✅ No active alerts - System Normal")
            
            print("\n📡 SIGNAL DISTRIBUTION:")
            for _, row in stats['signal_types'].iterrows():
                percentage = (row['count'] / stats['total_signals']) * 100
                print(f"   {row['signal_type']:12} : {row['count']:3} signals ({percentage:5.1f}%)")
            
            print("\n📶 FREQUENCY BAND ANALYSIS:")
            for _, row in stats['frequency_bands'].iterrows():
                band_percentage = (row['count'] / stats['total_signals']) * 100
                print(f"   {row['band']:15} : {row['count']:3} signals ({band_percentage:5.1f}%)")
            
            # Trend information
            if not trends.empty:
                current_rate = trends['signal_count'].iloc[-1] if len(trends) > 0 else 0
                avg_power = trends['avg_power'].mean() if len(trends) > 0 else 0
                print(f"\n📈 CURRENT TRENDS:")
                print(f"   Detection Rate : {current_rate:2} signals/min")
                print(f"   Average Power  : {avg_power:6.1f} dBm")
            
            print("\n🔍 RECENT SIGNAL ACTIVITY:")
            for _, row in stats['recent_activity'].iterrows():
                time_str = row['timestamp'][11:19] if 'timestamp' in row else 'N/A'
                freq_str = f"{row['frequency_mhz']:8.1f}" if 'frequency_mhz' in row else 'N/A'
                power_str = f"{row['power_dbm']:6.1f}" if 'power_dbm' in row else 'N/A'
                type_str = row['signal_type'] if 'signal_type' in row else 'N/A'
                print(f"   {time_str} - {freq_str} MHz - {power_str} dBm - {type_str}")
            
            print("\n" + "="*70)
            print("Press Ctrl+C to exit | Auto-refresh every 10 seconds")
            print("="*70)
            
            time.sleep(10)
    
    def get_realtime_stats(self):
        """Get real-time statistics (compatible with previous version)"""
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

if __name__ == "__main__":
    dashboard = EnhancedRFDashboard()
    try:
        dashboard.show_enhanced_dashboard()
    except KeyboardInterrupt:
        print("\n👋 Enhanced dashboard closed")
