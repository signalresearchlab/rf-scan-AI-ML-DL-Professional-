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
# auto_reporter.py - Automated Reporting System
import sqlite3
import pandas as pd
import json
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class AutoReporter:
    def __init__(self):
        self.db_path = 'saved_data/database/rf_scanner.db'
        self.reports_dir = 'saved_data/reports'
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def generate_daily_report(self):
        """Generate daily RF monitoring report"""
        conn = sqlite3.connect(self.db_path)
        
        # Get yesterday's date
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        
        # Daily statistics
        daily_stats = pd.read_sql(f'''
            SELECT 
                COUNT(*) as total_signals,
                AVG(power_dbm) as avg_power,
                MIN(power_dbm) as min_power,
                MAX(power_dbm) as max_power,
                COUNT(DISTINCT signal_type) as unique_signal_types
            FROM detected_signals 
            WHERE date(timestamp) = '{yesterday}'
        ''', conn)
        
        # Signal type breakdown
        signal_breakdown = pd.read_sql(f'''
            SELECT signal_type, COUNT(*) as count, 
                   AVG(power_dbm) as avg_power,
                   AVG(frequency_mhz) as avg_frequency
            FROM detected_signals 
            WHERE date(timestamp) = '{yesterday}'
            GROUP BY signal_type
            ORDER BY count DESC
        ''', conn)
        
        # Hourly activity
        hourly_activity = pd.read_sql(f'''
            SELECT strftime('%H:00', timestamp) as hour,
                   COUNT(*) as signal_count
            FROM detected_signals 
            WHERE date(timestamp) = '{yesterday}'
            GROUP BY hour
            ORDER BY hour
        ''', conn)
        
        conn.close()
        
        # Generate report
        report = {
            'report_date': datetime.now().strftime('%Y-%m-%d'),
            'analysis_period': yesterday,
            'summary': {
                'total_signals': int(daily_stats['total_signals'].iloc[0]),
                'average_power': float(daily_stats['avg_power'].iloc[0]),
                'power_range': f"{float(daily_stats['min_power'].iloc[0]):.1f} to {float(daily_stats['max_power'].iloc[0]):.1f} dBm",
                'unique_signal_types': int(daily_stats['unique_signal_types'].iloc[0])
            },
            'signal_breakdown': signal_breakdown.to_dict('records'),
            'hourly_activity': hourly_activity.to_dict('records'),
            'generated_at': datetime.now().isoformat()
        }
        
        # Save report
        report_file = f"{self.reports_dir}/daily_report_{yesterday}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Generate human-readable summary
        summary_file = f"{self.reports_dir}/daily_summary_{yesterday}.txt"
        with open(summary_file, 'w') as f:
            f.write(self._format_report_text(report))
        
        print(f"✅ Daily report generated: {report_file}")
        return report
    
    def _format_report_text(self, report):
        """Format report as human-readable text"""
        text = f"""
RF MONITORING DAILY REPORT
==========================

Date: {report['report_date']}
Analysis Period: {report['analysis_period']}
Generated: {report['generated_at']}

SUMMARY:
--------
• Total Signals: {report['summary']['total_signals']}
• Average Power: {report['summary']['average_power']:.1f} dBm  
• Power Range: {report['summary']['power_range']}
• Signal Types: {report['summary']['unique_signal_types']}

SIGNAL BREAKDOWN:
-----------------
"""
        for signal in report['signal_breakdown']:
            text += f"• {signal['signal_type']}: {signal['count']} signals, avg {signal['avg_power']:.1f} dBm\n"
        
        text += "\nHOURLY ACTIVITY:\n----------------\n"
        for hour_data in report['hourly_activity']:
            text += f"• {hour_data['hour']}: {hour_data['signal_count']} signals\n"
        
        text += f"\n--- End of Report ---"
        return text
    
    def start_auto_reporting(self):
        """Start automated reporting system"""
        print("📊 Starting Automated Reporting System...")
        print("Reports will be generated daily and saved to saved_data/reports/")
        
        # Generate initial report
        self.generate_daily_report()
        
        print("✅ Auto-reporter started. Reports will be generated daily.")
        print("💾 Check saved_data/reports/ for generated reports")

if __name__ == "__main__":
    reporter = AutoReporter()
    reporter.start_auto_reporting()
