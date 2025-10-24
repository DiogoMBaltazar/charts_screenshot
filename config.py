"""Configuration settings for TradingView screenshot pipeline."""

import os
from pathlib import Path

# Base configuration
BASE_DIR = Path(__file__).parent
SCREENSHOTS_DIR = BASE_DIR / "screenshots"
LOGS_DIR = BASE_DIR / "logs"

# Create directories if they don't exist
SCREENSHOTS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Cryptocurrency symbols and their TradingView URLs
CRYPTO_SYMBOLS = {
    "BTC": "https://www.tradingview.com/chart/?symbol=BINANCE%3ABTCUSDT",
    "ETH": "https://www.tradingview.com/chart/?symbol=BINANCE%3AETHUSDT", 
    "SOL": "https://www.tradingview.com/chart/?symbol=BINANCE%3ASOLUSDT"
}

# Screenshot settings
SCREENSHOT_WIDTH = 1920
SCREENSHOT_HEIGHT = 1080
SCREENSHOT_QUALITY = 100

# Browser settings
BROWSER_HEADLESS = True
BROWSER_TIMEOUT = 30000  # 30 seconds

# Scheduling settings
SCREENSHOT_INTERVAL_MINUTES = 1

# File naming
TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"
