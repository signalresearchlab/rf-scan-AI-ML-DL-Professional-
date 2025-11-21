#!/usr/bin/env python3
"""
RF Scanner AI - Main Entry Point
"""

import sys
import time
from datetime import datetime

def main():
    print("🚀 Advanced RF Scanning System Starting...")
    print("Available modes: monitor, sweep, spectrum, ml, cnn, dashboard, contact")
    
    # Check available modules
    modules = {
        "monitor": False,
        "sweep": False, 
        "spectrum": False,
        "ml": False,
        "cnn": False,
        "dashboard": False,
        "contact": False
    }
    
    # Test imports
    try:
        import monitor
        modules["monitor"] = True
    except ImportError:
        print("⚠️ Monitor module not available")
    
    try:
        import spectrum
        modules["spectrum"] = True
    except ImportError:
        print("⚠️ Spectrum module not available")
    
    try:
        import ml
        modules["ml"] = True
    except ImportError:
        print("⚠️ ML module not available")
    
    try:
        from cnn import train_cnn_model
        modules["cnn"] = True
    except ImportError:
        print("⚠️ CNN module not available")
    
    try:
        import web_dashboard_fixed
        modules["dashboard"] = True
    except ImportError:
        print("⚠️ Dashboard module not available")
    
    try:
        import contact_app
        modules["contact"] = True
    except ImportError:
        print("⚠️ Contact module not available")
    
    # Show available modes
    available_modes = [mode for mode, available in modules.items() if available]
    print(f"✅ Available modes: {', '.join(available_modes)}")
    
    mode = input("Enter mode: ").strip().lower()
    
    if mode == "monitor" and modules["monitor"]:
        print("📡 Starting RF Monitoring...")
        monitor.main()
        
    elif mode == "spectrum" and modules["spectrum"]:
        print("📊 Starting Spectrum Analysis...")
        spectrum.main()
        
    elif mode == "ml" and modules["ml"]:
        print("🤖 Starting Machine Learning Analysis...")
        ml.main()
        
    elif mode == "cnn" and modules["cnn"]:
        print("🧠 Starting CNN Deep Learning...")
        train_cnn_model()
        
    elif mode == "dashboard" and modules["dashboard"]:
        print("🌐 Starting Web Dashboard...")
        web_dashboard_fixed.main()
        
    elif mode == "contact" and modules["contact"]:
        print("📧 Starting Contact Form...")
        contact_app.main()
        
    else:
        print(f"❌ Mode '{mode}' not available or not implemented")
        print("💡 Try one of the available modes above")

if __name__ == "__main__":
    main()
