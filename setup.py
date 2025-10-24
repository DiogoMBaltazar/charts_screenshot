"""Setup script for TradingView screenshot pipeline."""

import subprocess
import sys
from pathlib import Path


def install_requirements():
    """Install Python requirements."""
    print("Installing Python requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Python requirements installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install Python requirements: {e}")
        return False
    return True


def install_playwright_browsers():
    """Install Playwright browser binaries."""
    print("Installing Playwright browsers...")
    try:
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
        print("✓ Playwright browsers installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install Playwright browsers: {e}")
        return False
    return True


def create_directories():
    """Create necessary directories."""
    print("Creating directories...")
    directories = ["screenshots", "logs"]
    
    for dir_name in directories:
        dir_path = Path(dir_name)
        dir_path.mkdir(exist_ok=True)
        print(f"✓ Created directory: {dir_path}")
    
    return True


def main():
    """Main setup function."""
    print("Setting up TradingView Screenshot Pipeline...")
    print("=" * 50)
    
    steps = [
        ("Installing Python requirements", install_requirements),
        ("Installing Playwright browsers", install_playwright_browsers),
        ("Creating directories", create_directories),
    ]
    
    for step_name, step_func in steps:
        print(f"\n{step_name}...")
        if not step_func():
            print(f"\n✗ Setup failed at: {step_name}")
            sys.exit(1)
    
    print("\n" + "=" * 50)
    print("✓ Setup completed successfully!")
    print("\nTo run the pipeline:")
    print("  python screenshot_pipeline.py")
    print("\nTo test a single screenshot capture:")
    print("  python tradingview_scraper.py")


if __name__ == "__main__":
    main()
