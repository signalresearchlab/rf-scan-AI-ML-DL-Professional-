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
# spectrum.py - Spectrum Analyzer with SQL Database
import numpy as np
import time
import json
import os
from datetime import datetime
from database_manager import DatabaseManager

class SpectrumAnalyzer:
    def __init__(self, freq_range=(1e6, 6e9), sample_rate=2e6):
        self.freq_range = freq_range
        self.sample_rate = sample_rate
        self.is_running = False
        self.spectrum_data = []
        self.db = DatabaseManager()
        self.setup_spectrum_files()
        
        print(f"📡 Spectrum Analyzer initialized")
        print(f"   Frequency range: {freq_range[0]/1e6} - {freq_range[1]/1e6} MHz")
        print(f"   Sample rate: {sample_rate/1e6} MHz")

    def setup_spectrum_files(self):
        """Setup files for spectrum data"""
        os.makedirs('saved_data/spectrum', exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.spectrum_file = f"saved_data/spectrum/spectrum_{timestamp}.csv"
        self.analysis_file = f"saved_data/spectrum/analysis_{timestamp}.json"
        
        with open(self.spectrum_file, 'w') as f:
            f.write("timestamp,peak_power,mean_power,peak_frequency,bandwidth\n")
        
        print(f"📁 Spectrum data will be saved to:")
        print(f"   CSV:  {self.spectrum_file}")
        print(f"   JSON: {self.analysis_file}")
        print(f"   SQL:  saved_data/database/rf_scanner.db")

    def save_spectrum_analysis(self, spectrum, peak_power, mean_power, peak_freq):
        """Save spectrum analysis results to both file and database"""
        timestamp = datetime.now().isoformat()
        
        # Save to CSV
        with open(self.spectrum_file, 'a') as f:
            f.write(f"{timestamp},{peak_power:.2f},{mean_power:.2f},{peak_freq},{len(spectrum)}\n")
        
        # Save to Database
        center_freq = np.random.uniform(self.freq_range[0], self.freq_range[1])
        bandwidth = self.sample_rate
        
        self.db.save_spectrum_analysis(
            center_freq, bandwidth, peak_power, mean_power,
            peak_freq, len(spectrum)
        )
        
        print(f"💾 Saved spectrum analysis: Peak {peak_power:.2f} dB at bin {peak_freq}")

    def save_complete_analysis(self):
        """Save complete analysis session"""
        session_data = {
            'session_info': {
                'start_time': datetime.now().isoformat(),
                'total_analyses': len(self.spectrum_data),
                'frequency_range': [self.freq_range[0], self.freq_range[1]],
                'sample_rate': self.sample_rate
            },
            'spectrum_data': self.spectrum_data
        }
        
        with open(self.analysis_file, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        # Log to database
        self.db.save_system_log('spectrum', 
                               f'Completed spectrum analysis session with {len(self.spectrum_data)} analyses',
                               'INFO', session_data)
        
        print(f"📁 Complete spectrum analysis saved to database")

    def simulate_sdr_capture(self):
        """Simulate SDR data capture without hardware"""
        t = np.linspace(0, 1, 1024)
        signal1 = 0.5 * np.sin(2 * np.pi * 100 * t)
        signal2 = 0.3 * np.sin(2 * np.pi * 200 * t)
        noise = 0.1 * np.random.randn(1024)
        
        iq_data = signal1 + signal2 + noise + 1j * (signal1 - signal2 + noise)
        return iq_data

    def compute_spectrum(self, iq_data):
        """Compute power spectrum from IQ data"""
        fft_result = np.fft.fft(iq_data)
        power_spectrum = 10 * np.log10(np.abs(fft_result)**2 + 1e-10)
        return power_spectrum

    def analyze_spectrum(self):
        """Perform spectrum analysis"""
        print(f"[{datetime.now()}] Analyzing spectrum...")
        
        iq_data = self.simulate_sdr_capture()
        spectrum = self.compute_spectrum(iq_data)
        
        max_power = np.max(spectrum)
        mean_power = np.mean(spectrum)
        peak_freq = np.argmax(spectrum)
        
        print(f"   📊 Spectrum Analysis:")
        print(f"   ├── Peak power: {max_power:.2f} dB")
        print(f"   ├── Mean power: {mean_power:.2f} dB") 
        print(f"   └── Peak frequency bin: {peak_freq}")
        
        self.save_spectrum_analysis(spectrum, max_power, mean_power, peak_freq)
        
        return spectrum

def main():
    """Main function for spectrum analysis"""
    print("Starting Spectrum Analyzer with SQL Database...")
    
    try:
        analyzer = SpectrumAnalyzer()
        print("✅ Spectrum Analyzer ready!")
        
        duration = int(input("Enter analysis duration in seconds (default 30): ") or "30")
        end_time = time.time() + duration
        
        analysis_count = 0
        while time.time() < end_time:
            analyzer.analyze_spectrum()
            analysis_count += 1
            time.sleep(2)
            
        analyzer.save_complete_analysis()
        print(f"\n✅ Completed {analysis_count} spectrum analyses saved to database")
        
    except KeyboardInterrupt:
        print("\n⏹️ Spectrum analysis stopped by user")
    except Exception as e:
        print(f"❌ Spectrum analysis error: {e}")

if __name__ == "__main__":
    main()
