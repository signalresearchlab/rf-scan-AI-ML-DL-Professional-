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
# monitor.py - RF Monitoring System with SQL Database
import schedule
import time
import json
import numpy as np
from datetime import datetime
import os
from database_manager import DatabaseManager

class RFMonitoringSystem:
    def __init__(self):
        print("RF Monitoring System Initialized")
        self.is_running = False
        self.scan_data = []
        self.detected_signals = []
        self.db = DatabaseManager()
        self.setup_data_files()
        
    def setup_data_files(self):
        """Setup data files for saving"""
        os.makedirs('saved_data/monitoring', exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.data_file = f"saved_data/monitoring/monitoring_{timestamp}.json"
        self.signals_file = f"saved_data/monitoring/signals_{timestamp}.csv"
        
        with open(self.signals_file, 'w') as f:
            f.write("timestamp,frequency_mhz,power_dbm,signal_type,modulation\n")
        
        print(f"📁 Data will be saved to:")
        print(f"   JSON: {self.data_file}")
        print(f"   CSV:  {self.signals_file}")
        print(f"   SQL:  saved_data/database/rf_scanner.db")

    def save_detected_signal(self, frequency, power, signal_type='unknown', modulation=None):
        """Save detected signal to both CSV and Database"""
        timestamp = datetime.now().isoformat()
        
        # Save to CSV
        with open(self.signals_file, 'a') as f:
            f.write(f"{timestamp},{frequency/1e6},{power:.2f},{signal_type},{modulation or 'unknown'}\n")
        
        # Save to Database
        confidence = np.random.uniform(0.7, 0.95)  # Simulate confidence
        bandwidth = np.random.uniform(1.0, 40.0)   # Simulate bandwidth in MHz
        
        self.db.save_detected_signal(
            frequency, power, signal_type, confidence, 
            bandwidth * 1e6, modulation  # Convert MHz to Hz
        )
        
        print(f"💾 Saved signal: {frequency/1e6:.1f} MHz, {power:.1f} dBm, {signal_type}")

    def save_scan_session(self):
        """Save complete scan session data"""
        session_data = {
            'session_start': datetime.now().isoformat(),
            'total_scans': len(self.scan_data),
            'signals_detected': len(self.detected_signals),
            'scan_data': self.scan_data,
            'detected_signals': self.detected_signals
        }
        
        with open(self.data_file, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        # End database session
        self.db.end_monitoring_session(len(self.scan_data))
        
        print(f"📁 Session data saved to: {self.data_file}")
        print(f"📊 Signals saved to database")

    def quick_scan(self):
        """Quick scan of common frequencies"""
        print(f"[{datetime.now()}] Quick scan - Checking common frequencies...")
        frequencies = [88e6, 433e6, 868e6, 2.4e9, 5.8e9]
        signal_types = ['FM', 'LORA', 'GSM', 'WIFI', 'RADAR']
        
        for i, freq in enumerate(frequencies):
            print(f"  📡 Scanning {freq/1e6} MHz")
            
            # Simulate signal detection during scan
            if np.random.random() > 0.7:
                power = np.random.uniform(-70, -40)
                self.save_detected_signal(freq, power, signal_types[i], signal_types[i])
            
            time.sleep(0.5)
    
    def deep_scan(self):
        """Deep frequency scan"""
        print(f"[{datetime.now()}] Deep scan - Comprehensive frequency analysis...")
        for i in range(3):
            print(f"  🔍 Deep scan segment {i+1}/3")
            
            # Simulate finding signals during deep scan
            if np.random.random() > 0.5:
                freq = np.random.uniform(100e6, 3e9)
                power = np.random.uniform(-80, -35)
                modulations = ['QPSK', 'BPSK', 'FSK', 'QAM16']
                modulation = np.random.choice(modulations)
                self.save_detected_signal(freq, power, 'DIGITAL', modulation)
            
            time.sleep(1)
    
    def spectral_analysis(self):
        """Spectral analysis task"""
        print(f"[{datetime.now()}] Performing spectral analysis...")
        
        # Simulate spectrum analysis and save to database
        center_freq = np.random.uniform(50e6, 6e9)
        bandwidth = np.random.uniform(1e6, 100e6)
        peak_power = np.random.uniform(-50, -20)
        mean_power = np.random.uniform(-80, -40)
        
        self.db.save_spectrum_analysis(
            center_freq, bandwidth, peak_power, mean_power,
            np.random.randint(0, 1024), 1024
        )
        
        signals_detected = np.random.randint(0, 5)
        print(f"  📊 Detected {signals_detected} signals")
    
    def generate_report(self):
        """Generate monitoring report"""
        print(f"[{datetime.now()}] Generating system report...")
        
        # Get recent signals from database
        recent_signals = self.db.get_recent_signals(5)
        
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'scan_count': len(self.scan_data),
            'signals_detected': len(self.detected_signals),
            'recent_signals': recent_signals
        }
        
        print(f"  📈 Report: {len(recent_signals)} recent signals in database")
        
        # Log to database
        self.db.save_system_log('monitor', 'Generated system report', 'INFO', report_data)
    
    def start_monitoring(self, duration=60):
        """Start the monitoring system"""
        print(f"🔄 Starting RF monitoring for {duration} seconds...")
        
        # Start database session
        self.db.start_monitoring_session(duration)
        
        schedule.every(1).minutes.do(self.quick_scan)
        schedule.every(3).minutes.do(self.deep_scan)
        schedule.every(5).minutes.do(self.spectral_analysis)
        schedule.every(10).minutes.do(self.generate_report)
        
        self.is_running = True
        start_time = time.time()
        
        # Log session start
        self.db.save_system_log('monitor', f'Started monitoring session for {duration} seconds')
        
        self.quick_scan()
        self.deep_scan()
        
        try:
            while self.is_running and (time.time() - start_time) < duration:
                schedule.run_pending()
                time.sleep(1)
                
                # Random signal detection
                if np.random.random() > 0.8:
                    freq = np.random.choice([88e6, 433e6, 868e6, 2.4e9, 5.8e9])
                    power = np.random.uniform(-80, -30)
                    signal_types = ['FM', 'WIFI', 'BLUETOOTH', 'UNKNOWN']
                    signal_type = np.random.choice(signal_types)
                    self.save_detected_signal(freq, power, signal_type)
                    
        except KeyboardInterrupt:
            print("\n⏹️ Monitoring stopped by user")
            self.db.save_system_log('monitor', 'Monitoring stopped by user', 'WARNING')
        finally:
            self.is_running = False
            self.save_scan_session()
            print("✅ Monitoring session completed and data saved to database!")

def main():
    """Main function for monitoring mode"""
    print("Starting RF Monitoring System with SQL Database...")
    monitor = RFMonitoringSystem()
    
    try:
        duration = int(input("Enter monitoring duration in seconds (default 60): ") or "60")
        monitor.start_monitoring(duration)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user")
    except Exception as e:
        print(f"Monitoring error: {e}")

if __name__ == "__main__":
    main()
