#!/bin/bash

echo "🚀 Installing RF-Scan AI/ML/DL Professional..."

# Check if Python 3.8+ is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv .venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Install package in development mode
echo "🔨 Installing package..."
pip install -e .

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p saved_data/database
mkdir -p saved_data/monitoring
mkdir -p saved_data/spectrum
mkdir -p saved_data/reports
mkdir -p saved_data/models

# Initialize database
echo "🗄️ Initializing database..."
python3 database_setup.py

echo "✅ Installation complete!"
echo ""
echo "🎯 To get started:"
echo "   source .venv/bin/activate"
echo "   rf-scan --help"
echo "   python3 web_dashboard_fixed.py"
echo ""
echo "📚 Available commands:"
echo "   rf-scan          - Main CLI interface"
echo "   rf-scan-dashboard - Web dashboard"
echo "   rf-scan-monitor   - Real-time monitoring"
