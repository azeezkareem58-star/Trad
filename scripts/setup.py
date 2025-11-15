#!/usr/bin/env python3
import os
import sys
import subprocess

def run_command(command):
    """Execute shell command"""
    try:
        subprocess.run(command, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing: {command}")
        return False

def setup_project():
    """Setup the trading bot project"""
    print("🚀 Setting up Bybit Trading Bot...")
    
    # Check if Python is available
    if not run_command("python --version"):
        print("❌ Python is not installed or not in PATH")
        return
    
    # Create virtual environment
    print("📦 Creating virtual environment...")
    if not run_command("python -m venv venv"):
        return
    
    # Install requirements
    print("📚 Installing dependencies...")
    if os.name == 'nt':  # Windows
        pip_cmd = "venv\\Scripts\\pip"
    else:  # Unix/Linux/Mac
        pip_cmd = "venv/bin/pip"
    
    if not run_command(f"{pip_cmd} install -r requirements.txt"):
        return
    
    # Create .env file if it doesn't exist
    if not os.path.exists('.env') and os.path.exists('.env.example'):
        print("🔐 Creating .env file from template...")
        run_command("cp .env.example .env")
        print("📝 Please edit .env file with your API keys")
    
    print("✅ Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env file with your API keys")
    print("2. Activate virtual environment:")
    if os.name == 'nt':
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print("3. Run: python trading_bot.py")

if __name__ == "__main__":
    setup_project()