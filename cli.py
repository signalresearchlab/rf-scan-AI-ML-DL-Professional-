#!/usr/bin/env python3
"""
RF Scanner AI - Command Line Interface
"""

import click
import os
import sys
import subprocess
from pathlib import Path

@click.group()
@click.version_option(version="1.0.0")
def cli():
    """RF Scanner AI - Advanced RF Signal Detection & Analysis"""
    pass

@cli.command()
def install():
    """Install RF Scanner AI and all dependencies"""
    click.echo("🚀 Installing RF Scanner AI...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        click.echo("❌ Python 3.8+ is required")
        return
    
    # Create virtual environment
    if not Path(".venv").exists():
        click.echo("📦 Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", ".venv"])
    
    # Determine activation command
    if os.name == 'nt':  # Windows
        activate_cmd = ".venv\\Scripts\\activate"
        pip_cmd = ".venv\\Scripts\\pip"
        python_cmd = ".venv\\Scripts\\python"
    else:  # Linux/Mac
        activate_cmd = "source .venv/bin/activate"
        pip_cmd = ".venv/bin/pip"
        python_cmd = ".venv/bin/python"
    
    # Install dependencies
    click.echo("📚 Installing dependencies...")
    subprocess.run([pip_cmd, "install", "--upgrade", "pip"])
    subprocess.run([pip_cmd, "install", "-r", "requirements.txt"])
    
    # Install package in development mode
    click.echo("🔨 Installing package...")
    subprocess.run([pip_cmd, "install", "-e", "."])
    
    # Create necessary directories
    click.echo("📁 Creating directories...")
    directories = [
        "saved_data/database",
        "saved_data/monitoring", 
        "saved_data/spectrum",
        "saved_data/ml",
        "saved_data/cnn", 
        "saved_data/reports",
        "saved_data/models",
        "templates"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    # Initialize database
    click.echo("🗄️ Initializing database...")
    subprocess.run([python_cmd, "database_setup.py"])
    
    click.echo("✅ Installation complete!")
    click.echo("\n🎯 Quick start:")
    click.echo("   rf-scan --help")
    click.echo("   rf-scan start")

@cli.command()
def start():
    """Start the main RF monitoring system"""
    click.echo("🚀 Starting RF Scanner AI...")
    subprocess.run([sys.executable, "start.py"])

@cli.command()
@click.option('--host', default='127.0.0.1', help='Host to bind the dashboard')
@click.option('--port', default=5000, help='Port to bind the dashboard')
def dashboard(host, port):
    """Start the web dashboard"""
    click.echo(f"🌐 Starting web dashboard on {host}:{port}...")
    os.environ['FLASK_HOST'] = host
    os.environ['FLASK_PORT'] = str(port)
    subprocess.run([sys.executable, "web_dashboard_fixed.py"])

@cli.command()
@click.option('--host', default='127.0.0.1', help='Host for contact form')
@click.option('--port', default=5001, help='Port for contact form')
def contact(host, port):
    """Start the contact form server"""
    click.echo(f"📧 Starting contact form on {host}:{port}...")
    os.environ['CONTACT_HOST'] = host
    os.environ['CONTACT_PORT'] = str(port)
    subprocess.run([sys.executable, "contact_app.py"])

@cli.command()
def monitor():
    """Start real-time RF monitoring"""
    click.echo("📡 Starting RF monitoring...")
    subprocess.run([sys.executable, "monitor.py"])

@cli.command()
def alerts():
    """Start the alert system"""
    click.echo("🚨 Starting alert system...")
    subprocess.run([sys.executable, "alerts.py"])

@cli.command()
@click.option('--frequency', '-f', help='Frequency to scan (e.g., 2.4G)')
@click.option('--duration', '-d', default=10, help='Scan duration in seconds')
def scan(frequency, duration):
    """Perform RF spectrum scan"""
    cmd = [sys.executable, "spectrum.py"]
    if frequency:
        cmd.extend(["--frequency", frequency])
    if duration:
        cmd.extend(["--duration", str(duration)])
    subprocess.run(cmd)

@cli.command()
@click.option('--train', is_flag=True, help='Train ML models')
@click.option('--predict', is_flag=True, help='Run predictions')
def ml(train, predict):
    """Machine Learning operations"""
    cmd = [sys.executable, "ml.py"]
    if train:
        cmd.append("--train")
    if predict:
        cmd.append("--predict")
    subprocess.run(cmd)

@cli.command()
def quickstart():
    """Start all services at once"""
    click.echo("🎯 Starting all RF Scanner AI services...")
    subprocess.run([sys.executable, "quick_start.py"])

@cli.command()
def status():
    """Check system status"""
    click.echo("🔍 Checking RF Scanner AI status...")
    
    # Check if virtual environment exists
    venv_exists = Path(".venv").exists()
    click.echo(f"📦 Virtual environment: {'✅ Exists' if venv_exists else '❌ Missing'}")
    
    # Check if database exists
    db_exists = Path("saved_data/database/rf_signals.db").exists()
    click.echo(f"🗄️ Database: {'✅ Exists' if db_exists else '❌ Missing'}")
    
    # Check main modules
    modules = [
        ("start.py", "Main system"),
        ("monitor.py", "RF Monitor"), 
        ("web_dashboard_fixed.py", "Web Dashboard"),
        ("contact_app.py", "Contact Form")
    ]
    
    for module, description in modules:
        exists = Path(module).exists()
        click.echo(f"🔧 {description}: {'✅ Ready' if exists else '❌ Missing'}")

if __name__ == '__main__':
    cli()
