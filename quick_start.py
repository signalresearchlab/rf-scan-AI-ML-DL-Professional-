#!/usr/bin/env python3
"""
Quick Start Script for RF-Scan AI/ML/DL Professional
Starts all services simultaneously
"""

import subprocess
import sys
import threading
import time
import webbrowser
from typing import List

def run_command(command: List[str], name: str):
    """Run a command in subprocess"""
    print(f"🚀 Starting {name}...")
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process
    except Exception as e:
        print(f"❌ Failed to start {name}: {e}")
        return None

def main():
    """Start all RF-Scan services"""
    print("🎯 RF-Scan AI/ML/DL Professional - Quick Start")
    print("=" * 50)
    
    processes = []
    
    # Start web dashboard
    web_process = run_command([sys.executable, "web_dashboard_fixed.py"], "Web Dashboard")
    if web_process:
        processes.append(("Web Dashboard", web_process))
        time.sleep(2)  # Give web server time to start
        webbrowser.open("http://localhost:5000")
    
    # Start alert system
    alert_process = run_command([sys.executable, "alerts.py"], "Alert System")
    if alert_process:
        processes.append(("Alert System", alert_process))
    
    # Start enhanced dashboard
    dashboard_process = run_command([sys.executable, "enhanced_dashboard.py"], "Terminal Dashboard")
    if dashboard_process:
        processes.append(("Terminal Dashboard", dashboard_process))
    
    # Start main monitoring
    monitor_process = run_command([sys.executable, "start.py"], "Main RF System")
    if monitor_process:
        processes.append(("Main RF System", monitor_process))
    
    print("\n✅ All services started!")
    print("📊 Web Dashboard: http://localhost:5000")
    print("📧 Contact Form: http://localhost:5001")
    print("🛑 Press Ctrl+C to stop all services")
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping all services...")
        for name, process in processes:
            if process:
                process.terminate()
                print(f"✅ Stopped {name}")

if __name__ == "__main__":
    main()
