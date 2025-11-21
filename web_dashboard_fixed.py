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
# web_dashboard_fixed.py - Fixed Web Dashboard
from flask import Flask, render_template, jsonify
import sqlite3
import pandas as pd
import threading
import time
from datetime import datetime
import os
import json

app = Flask(__name__)

class WebDashboard:
    def __init__(self):
        self.db_path = 'saved_data/database/rf_scanner.db'
        self.latest_data = self.get_initial_data()
    
    def get_initial_data(self):
        """Get initial data"""
        return {
            'total_signals': 0,
            'today_signals': 0,
            'signal_types': [],
            'recent_signals': [],
            'frequency_bands': [],
            'last_update': 'Never'
        }
    
    def update_data(self):
        """Continuously update data in background"""
        while True:
            try:
                conn = sqlite3.connect(self.db_path)
                
                # Get latest stats
                total_signals = pd.read_sql('SELECT COUNT(*) as count FROM detected_signals', conn).iloc[0]['count']
                today_signals = pd.read_sql('''SELECT COUNT(*) as count FROM detected_signals 
                                            WHERE date(timestamp) = date('now')''', conn).iloc[0]['count']
                
                signal_types = pd.read_sql('''SELECT signal_type, COUNT(*) as count 
                                           FROM detected_signals GROUP BY signal_type''', conn)
                recent_signals = pd.read_sql('''SELECT timestamp, frequency_mhz, power_dbm, signal_type, modulation_type 
                                             FROM detected_signals 
                                             ORDER BY timestamp DESC LIMIT 10''', conn)
                frequency_bands = pd.read_sql('''SELECT 
                    CASE 
                        WHEN frequency_mhz < 300 THEN 'VHF'
                        WHEN frequency_mhz BETWEEN 300 AND 1000 THEN 'UHF' 
                        WHEN frequency_mhz BETWEEN 1000 AND 3000 THEN 'L-Band'
                        ELSE 'S-Band+'
                    END as band,
                    COUNT(*) as count
                    FROM detected_signals 
                    GROUP BY band''', conn)
                
                conn.close()
                
                self.latest_data = {
                    'total_signals': int(total_signals),
                    'today_signals': int(today_signals),
                    'signal_types': signal_types.to_dict('records'),
                    'recent_signals': recent_signals.to_dict('records'),
                    'frequency_bands': frequency_bands.to_dict('records'),
                    'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                print(f"📊 Data updated at {self.latest_data['last_update']} - {total_signals} total signals")
                
            except Exception as e:
                print(f"❌ Web dashboard update error: {e}")
                self.latest_data['last_update'] = f"Error: {str(e)}"
            
            time.sleep(5)  # Update every 5 seconds

# Initialize dashboard
dashboard = WebDashboard()

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>RF Monitoring Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .dashboard { max-width: 1200px; margin: 0 auto; }
        .header { background: #2c3e50; color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 20px; }
        .stat-card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); text-align: center; }
        .chart-container { background: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .signal-list { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .signal-item { padding: 10px; border-bottom: 1px solid #eee; }
        .signal-item:last-child { border-bottom: none; }
        .high-power { color: #e74c3c; font-weight: bold; }
        .unknown-signal { color: #f39c12; font-weight: bold; }
        .stat-number { font-size: 2.5em; font-weight: bold; margin: 10px 0; }
        .stat-label { color: #7f8c8d; font-size: 0.9em; }
    </style>
</head>
<body>
    <div class="dashboard">
        <div class="header">
            <h1>🛰️ RF Signal Monitoring Dashboard</h1>
            <p>Real-time RF signal detection and analysis</p>
            <div>Last update: <span id="updateTime">Loading...</span></div>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number" id="totalSignals">0</div>
                <div class="stat-label">Total Signals</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="todaySignals">0</div>
                <div class="stat-label">Today's Signals</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="signalTypes">0</div>
                <div class="stat-label">Signal Types</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="frequencyBands">0</div>
                <div class="stat-label">Frequency Bands</div>
            </div>
        </div>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
            <div class="chart-container">
                <h3>Signal Type Distribution</h3>
                <canvas id="signalTypeChart" width="400" height="300"></canvas>
            </div>
            <div class="chart-container">
                <h3>Frequency Band Distribution</h3>
                <canvas id="frequencyChart" width="400" height="300"></canvas>
            </div>
        </div>
        
        <div class="signal-list">
            <h3>Recent Signals</h3>
            <div id="recentSignals">
                <div class="signal-item">Loading recent signals...</div>
            </div>
        </div>
    </div>

    <script>
        let signalTypeChart, frequencyChart;
        
        function updateDashboard() {
            fetch('/api/data')
                .then(response => {
                    if (!response.ok) throw new Error('Network response was not ok');
                    return response.json();
                })
                .then(data => {
                    console.log('Data received:', data);
                    
                    // Update basic stats
                    document.getElementById('totalSignals').textContent = data.total_signals.toLocaleString();
                    document.getElementById('todaySignals').textContent = data.today_signals.toLocaleString();
                    document.getElementById('signalTypes').textContent = data.signal_types.length;
                    document.getElementById('frequencyBands').textContent = data.frequency_bands.length;
                    document.getElementById('updateTime').textContent = data.last_update;
                    
                    // Update charts
                    updateCharts(data);
                    
                    // Update recent signals
                    updateRecentSignals(data.recent_signals);
                })
                .catch(error => {
                    console.error('Error fetching data:', error);
                    document.getElementById('updateTime').textContent = 'Error loading data';
                });
        }
        
        function updateCharts(data) {
            // Signal Type Chart
            const signalTypeCtx = document.getElementById('signalTypeChart').getContext('2d');
            if (signalTypeChart) signalTypeChart.destroy();
            
            if (data.signal_types && data.signal_types.length > 0) {
                signalTypeChart = new Chart(signalTypeCtx, {
                    type: 'doughnut',
                    data: {
                        labels: data.signal_types.map(s => s.signal_type),
                        datasets: [{
                            data: data.signal_types.map(s => s.count),
                            backgroundColor: ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6', '#1abc9c']
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: {
                                position: 'bottom'
                            }
                        }
                    }
                });
            }
            
            // Frequency Band Chart
            const frequencyCtx = document.getElementById('frequencyChart').getContext('2d');
            if (frequencyChart) frequencyChart.destroy();
            
            if (data.frequency_bands && data.frequency_bands.length > 0) {
                frequencyChart = new Chart(frequencyCtx, {
                    type: 'bar',
                    data: {
                        labels: data.frequency_bands.map(b => b.band),
                        datasets: [{
                            label: 'Signal Count',
                            data: data.frequency_bands.map(b => b.count),
                            backgroundColor: '#3498db'
                        }]
                    },
                    options: {
                        responsive: true,
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                });
            }
        }
        
        function updateRecentSignals(signals) {
            const container = document.getElementById('recentSignals');
            
            if (!signals || signals.length === 0) {
                container.innerHTML = '<div class="signal-item">No signals detected yet</div>';
                return;
            }
            
            container.innerHTML = '';
            
            signals.forEach(signal => {
                const item = document.createElement('div');
                item.className = 'signal-item';
                
                const time = new Date(signal.timestamp).toLocaleTimeString();
                const power = parseFloat(signal.power_dbm);
                const freq = parseFloat(signal.frequency_mhz);
                
                let powerClass = '';
                if (power > -40) powerClass = 'high-power';
                if (signal.signal_type === 'UNKNOWN') powerClass = 'unknown-signal';
                
                item.innerHTML = `
                    <strong>${time}</strong> - 
                    <span>${freq.toFixed(1)} MHz</span> - 
                    <span class="${powerClass}">${power.toFixed(1)} dBm</span> - 
                    <span>${signal.signal_type}</span>
                    ${signal.modulation_type ? ` - <em>${signal.modulation_type}</em>` : ''}
                `;
                
                container.appendChild(item);
            });
        }
        
        // Initial load
        updateDashboard();
        
        // Update every 5 seconds
        setInterval(updateDashboard, 5000);
    </script>
</body>
</html>
""")

@app.route('/api/data')
def api_data():
    """API endpoint for dashboard data"""
    return jsonify(dashboard.latest_data)

def render_template_string(template_string):
    """Helper to render template from string"""
    from flask import render_template_string as rts
    return rts(template_string)

if __name__ == '__main__':
    # Start background data updates
    update_thread = threading.Thread(target=dashboard.update_data, daemon=True)
    update_thread.start()
    
    print("🌐 Starting Fixed Web Dashboard...")
    print("📊 Access at: http://localhost:5000")
    print("📡 Data will auto-update every 5 seconds")
    print("🛑 Press Ctrl+C to stop")
    
    app.run(debug=False, host='0.0.0.0', port=5000, use_reloader=False)
