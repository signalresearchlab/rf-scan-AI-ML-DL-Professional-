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
# analytics.py - Advanced RF Signal Analytics
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class RFAnalytics:
    def __init__(self):
        self.db_path = 'saved_data/database/rf_scanner.db'
    
    def time_series_analysis(self):
        """Analyze signal patterns over time"""
        conn = sqlite3.connect(self.db_path)
        
        # Get hourly signal counts
        df = pd.read_sql('''
            SELECT strftime('%Y-%m-%d %H:00:00', timestamp) as hour,
                   COUNT(*) as signal_count,
                   AVG(power_dbm) as avg_power
            FROM detected_signals 
            GROUP BY hour
            ORDER BY hour
        ''', conn)
        
        conn.close()
        
        if not df.empty:
            plt.figure(figsize=(12, 6))
            plt.plot(pd.to_datetime(df['hour']), df['signal_count'], marker='o')
            plt.title('RF Signals Over Time')
            plt.xlabel('Time')
            plt.ylabel('Signal Count')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig('saved_data/analytics/time_series.png')
            plt.show()
            
            return df
        return None
    
    def frequency_analysis(self):
        """Analyze frequency distribution"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql('SELECT frequency_mhz, power_dbm, signal_type FROM detected_signals', conn)
        conn.close()
        
        if not df.empty:
            plt.figure(figsize=(12, 6))
            
            # Create frequency bands
            bands = ['VHF (<300)', 'UHF (300-1000)', 'L-Band (1-3GHz)', 'S-Band+ (>3GHz)']
            band_counts = [
                len(df[df['frequency_mhz'] < 300]),
                len(df[(df['frequency_mhz'] >= 300) & (df['frequency_mhz'] < 1000)]),
                len(df[(df['frequency_mhz'] >= 1000) & (df['frequency_mhz'] < 3000)]),
                len(df[df['frequency_mhz'] >= 3000])
            ]
            
            plt.subplot(1, 2, 1)
            plt.pie(band_counts, labels=bands, autopct='%1.1f%%')
            plt.title('Signal Distribution by Frequency Band')
            
            plt.subplot(1, 2, 2)
            for signal_type in df['signal_type'].unique():
                type_data = df[df['signal_type'] == signal_type]
                plt.scatter(type_data['frequency_mhz'], type_data['power_dbm'], 
                           label=signal_type, alpha=0.6)
            
            plt.xlabel('Frequency (MHz)')
            plt.ylabel('Power (dBm)')
            plt.title('Signal Power vs Frequency')
            plt.legend()
            plt.tight_layout()
            plt.savefig('saved_data/analytics/frequency_analysis.png')
            plt.show()
            
            return df
        return None
    
    def signal_correlation(self):
        """Find correlations in signal data"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql('''
            SELECT frequency_mhz, power_dbm, 
                   CASE signal_type
                     WHEN 'WIFI' THEN 1
                     WHEN 'FM' THEN 2  
                     WHEN 'DIGITAL' THEN 3
                     ELSE 4
                   END as signal_type_code
            FROM detected_signals
        ''', conn)
        conn.close()
        
        if not df.empty:
            correlation = df.corr()
            print("\n📈 Signal Data Correlation Matrix:")
            print(correlation)
            
            return correlation
        return None
    
    def generate_report(self):
        """Generate comprehensive analytics report"""
        import os
        os.makedirs('saved_data/analytics', exist_ok=True)
        
        print("📊 Generating RF Analytics Report...")
        
        # Run all analyses
        time_data = self.time_series_analysis()
        freq_data = self.frequency_analysis()  
        correlation = self.signal_correlation()
        
        # Generate text report
        report = f"""
RF SCANNING ANALYTICS REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

SUMMARY:
- Total signals analyzed: {len(freq_data) if freq_data is not None else 0}
- Time period coverage: {len(time_data) if time_data is not None else 0} hours
- Frequency range: {freq_data['frequency_mhz'].min() if freq_data is not None else 0:.1f} - {freq_data['frequency_mhz'].max() if freq_data is not None else 0:.1f} MHz

KEY INSIGHTS:
- Most common signal type: {freq_data['signal_type'].mode()[0] if freq_data is not None else 'N/A'}
- Average signal power: {freq_data['power_dbm'].mean() if freq_data is not None else 0:.1f} dBm
- Signal detection rate: {len(freq_data)/24 if freq_data is not None else 0:.1f} signals/hour

CORRELATIONS:
Frequency vs Power: {correlation.iloc[0,1] if correlation is not None else 0:.3f}
        """
        
        with open('saved_data/analytics/report.txt', 'w') as f:
            f.write(report)
        
        print("✅ Analytics report generated: saved_data/analytics/report.txt")
        return report

if __name__ == "__main__":
    analytics = RFAnalytics()
    analytics.generate_report()
