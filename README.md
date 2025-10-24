# TradingView Screenshot Pipeline

An automated pipeline that captures high-resolution screenshots from TradingView charts for Bitcoin (BTC), Ethereum (ETH), and Solana (SOL) every minute.

## Features

- 🚀 Automated screenshot capture every minute
- 📊 Supports BTC, ETH, and SOL charts from TradingView
- 🖼️ High-resolution screenshots (1920x1080)
- 📁 Organized file storage with timestamps
- 🔄 Robust error handling and retry logic
- 📝 Comprehensive logging
- ⚡ Async/await for optimal performance

## Quick Start

1. **Setup the environment:**
   ```bash
   python setup.py
   ```

2. **Run the pipeline:**
   ```bash
   python screenshot_pipeline.py
   ```

3. **Test single capture (optional):**
   ```bash
   python tradingview_scraper.py
   ```

## Project Structure

```
chart_screenshot/
├── config.py              # Configuration settings
├── tradingview_scraper.py  # Browser automation and screenshot logic
├── screenshot_pipeline.py  # Main pipeline with scheduling
├── setup.py               # Setup script
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── screenshots/          # Generated screenshots (created automatically)
└── logs/                # Pipeline logs (created automatically)
```

## Configuration

Edit `config.py` to customize:

- **Cryptocurrency symbols and URLs**
- **Screenshot dimensions and quality**
- **Capture interval (default: 1 minute)**
- **Browser settings**
- **File naming conventions**

## Screenshot Naming

Screenshots are saved with the following naming pattern:
```
{SYMBOL}_{TIMESTAMP}.png
```

Example: `BTC_20241024_143052.png`

## Dependencies

- **Playwright**: Browser automation
- **APScheduler**: Task scheduling
- **Pillow**: Image processing
- **python-dotenv**: Environment configuration

## Stopping the Pipeline

Press `Ctrl+C` to gracefully stop the pipeline. The system will:
- Complete any ongoing screenshot capture
- Close browser instances
- Save final logs
- Exit cleanly

## Troubleshooting

### Common Issues

1. **Browser fails to start:**
   - Run `python -m playwright install chromium`
   - Check system requirements for Playwright

2. **TradingView pages don't load:**
   - Check internet connection
   - Verify TradingView URLs in `config.py`
   - Increase `BROWSER_TIMEOUT` in config

3. **Screenshots are blank:**
   - TradingView may have anti-bot measures
   - Try running with `BROWSER_HEADLESS = False` for debugging
   - Check if charts are loading properly

### Logs

Check the `logs/` directory for detailed pipeline logs:
- `pipeline_YYYYMMDD.log` - Daily pipeline logs
- Console output shows real-time status

## Customization

### Adding New Cryptocurrencies

Edit `CRYPTO_SYMBOLS` in `config.py`:

```python
CRYPTO_SYMBOLS = {
    "BTC": "https://www.tradingview.com/chart/?symbol=BINANCE%3ABTCUSDT",
    "ETH": "https://www.tradingview.com/chart/?symbol=BINANCE%3AETHUSDT",
    "SOL": "https://www.tradingview.com/chart/?symbol=BINANCE%3ASOLUSDT",
    "ADA": "https://www.tradingview.com/chart/?symbol=BINANCE%3AADAUSDT",  # New
}
```

### Changing Capture Interval

Modify `SCREENSHOT_INTERVAL_MINUTES` in `config.py`:

```python
SCREENSHOT_INTERVAL_MINUTES = 5  # Capture every 5 minutes
```

### Screenshot Quality

Adjust resolution and quality in `config.py`:

```python
SCREENSHOT_WIDTH = 2560
SCREENSHOT_HEIGHT = 1440
SCREENSHOT_QUALITY = 95
```

## License

This project is for educational and personal use. Please respect TradingView's terms of service.
