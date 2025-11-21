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
# alerts.py - Smart Alert System for RF Signals
import sqlite3
import time
from datetime import datetime

class RFAlertSystem:
    def __init__(self):
        self.db_path = 'saved_data/database/rf_scanner.db'
        self.alert_rules = {
            'high_power': {'threshold': -40, 'message': '🚨 HIGH POWER SIGNAL DETECTED'},
            'unknown_signal': {'message': '🔍 UNKNOWN SIGNAL TYPE DETECTED'},
            'unusual_frequency': {'min_freq': 5000, 'message': '📡 UNUSUAL FREQUENCY DETECTED'},
            'signal_burst': {'count_threshold': 3, 'time_window': 10, 'message': '⚡ SIGNAL BURST DETECTED'}
        }
    
    def check_alerts(self):
        """Check for alert conditions"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        alerts = []
        
        # Check for high power signals (last 5 minutes)
        cursor.execute('''
            SELECT timestamp, frequency_mhz, power_dbm, signal_type 
            FROM detected_signals 
            WHERE power_dbm > ? AND timestamp > datetime('now', '-5 minutes')
            ORDER BY timestamp DESC
        ''', (self.alert_rules['high_power']['threshold'],))
        
        high_power_signals = cursor.fetchall()
        for signal in high_power_signals:
            alerts.append({
                'type': 'high_power',
                'message': f"{self.alert_rules['high_power']['message']}: {signal[2]:.1f} dBm at {signal[1]:.1f} MHz",
                'timestamp': signal[0],
                'severity': 'HIGH'
            })
        
        # Check for unknown signals
        cursor.execute('''
            SELECT timestamp, frequency_mhz, power_dbm 
            FROM detected_signals 
            WHERE signal_type = 'UNKNOWN' AND timestamp > datetime('now', '-10 minutes')
            ORDER BY timestamp DESC
        ''')
        
        unknown_signals = cursor.fetchall()
        for signal in unknown_signals:
            alerts.append({
                'type': 'unknown_signal', 
                'message': f"{self.alert_rules['unknown_signal']['message']}: {signal[1]:.1f} MHz",
                'timestamp': signal[0],
                'severity': 'MEDIUM'
            })
        
        # Check for unusual frequencies
        cursor.execute('''
            SELECT timestamp, frequency_mhz, power_dbm, signal_type
            FROM detected_signals 
            WHERE frequency_mhz > ? AND timestamp > datetime('now', '-15 minutes')
            ORDER BY timestamp DESC
        ''', (self.alert_rules['unusual_frequency']['min_freq'],))
        
        unusual_freqs = cursor.fetchall()
        for signal in unusual_freqs:
            alerts.append({
                'type': 'unusual_frequency',
                'message': f"{self.alert_rules['unusual_frequency']['message']}: {signal[1]:.1f} MHz",
                'timestamp': signal[0],
                'severity': 'LOW'
            })
        
        conn.close()
        return alerts
    
    def start_alert_monitor(self):
        """Start continuous alert monitoring"""
        print("🚨 RF Alert System Started")
        print("Monitoring for: High power, Unknown signals, Unusual frequencies")
        print("=" * 50)
        
        while True:
            try:
                current_alerts = self.check_alerts()
                
                if current_alerts:
                    print(f"\n📢 ALERTS DETECTED [{datetime.now().strftime('%H:%M:%S')}]:")
                    for alert in current_alerts:
                        print(f"   {alert['severity']}: {alert['message']}")
                else:
                    print(f"✅ No alerts [{datetime.now().strftime('%H:%M:%S')}] - System Normal")
                
                time.sleep(30)  # Check every 30 seconds
                
            except KeyboardInterrupt:
                print("\n🛑 Alert system stopped")
                break
            except Exception as e:
                print(f"❌ Alert system error: {e}")
                time.sleep(30)

if __name__ == "__main__":
    alert_system = RFAlertSystem()
    alert_system.start_alert_monitor()
